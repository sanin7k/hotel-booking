import React, { useState } from "react";
import api from "../api/axios";
import { useNavigate } from "react-router-dom";

export default function Register() {
  const navigate = useNavigate();
  const [form, setForm] = useState({
    username: "",
    email: "",
    password: "",
    confirm_password: "",
  });
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");

  const handleChange = (e) => {
    setForm((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    setError("");
    setMessage("");

    try {
      const response = await api.post("/auth/register", form);
      setMessage(response.data.message || "Registration successful");
      navigate("/verify-email");
    } catch (error) {
      setError(error.response?.data?.detail || "Registration failed");
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <form
        onSubmit={handleRegister}
        className="bg-white p-8 rounded-lg shadow-md w-full max-w-md"
      >
        <h2 className="text-2xl font-bold mb-6 text-center">Register</h2>

        {error && <div className="text-red-500 text-sm mb-4">{error}</div>}
        {message && (
          <div className="text-green-500 text-sm mb-4">{message}</div>
        )}

        <div className="mb-4">
          <label className="block mb-1 text-left">Username</label>
          <input
            type="text"
            name="username"
            className="w-full px-4 py-2 border rounded"
            value={form.username}
            onChange={handleChange}
            required
          />
        </div>

        <div className="mb-4">
          <label className="block mb-1 text-left">Email</label>
          <input
            type="email"
            name="email"
            className="w-full px-4 py-2 border rounded"
            value={form.email}
            onChange={handleChange}
            required
          />
        </div>

        <div className="mb-4">
          <label className="block mb-1 text-left">Password</label>
          <input
            type="password"
            name="password"
            className="w-full px-4 py-2 border rounded"
            value={form.password}
            onChange={handleChange}
            required
          />
        </div>

        <div className="mb-4">
          <label className="block mb-1 text-left">Confirm Password</label>
          <input
            type="password"
            name="confirm_password"
            className="w-full px-4 py-2 border rounded"
            value={form.confirm_password}
            onChange={handleChange}
            required
          />
        </div>

        <button
          type="submit"
          className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 transition"
        >
          Register
        </button>

        <p className="text-sm mt-4 text-center">
          Already have an account?{" "}
          <a href="/login" className="text-blue-600 hover:underline">
            Login
          </a>
        </p>
      </form>
    </div>
  );
}
