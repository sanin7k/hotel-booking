import React, { useEffect, useState } from "react";
import api from "../api/axios";
import { Link, useNavigate } from "react-router-dom";

import GoogleLogin from "../components/GoogleLogin";

export default function Login() {
  const navigate = useNavigate();
  const [form, setForm] = useState({
    email: "",
    password: "",
  });
  const [error, setError] = useState("");

  const handleChange = (e) => {
    setForm((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    setError("");

    try {
      await api.post("/auth/login", form);
      navigate("/dashboard");
    } catch (error) {
      setError(error.response?.data?.detail || "Login failed");
    }
  };

  useEffect(() => {
    const redirect = async() => {
      const response = await api.get("/logged_in");
      const logged_in = response.data.logged_in
      if (logged_in) {
        navigate("/dashboard");
      } 
    };

    redirect();
  }, [navigate]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="bg-white p-8 rounded-lg shadow-md w-full max-w-md flex flex-col">
        <form onSubmit={handleLogin}>
          <h2 className="text-2xl font-bold mb-6 text-center">Login</h2>

          {error && <div className="text-red-500 text-sm mb-4">{error}</div>}

          <div className="mb-4">
            <label className="block mb-1 text-left">Email</label>
            <input
              className="w-full px-4 py-2 border rounded"
              name="email"
              type="email"
              value={form.email}
              onChange={handleChange}
              required
            />
          </div>

          <div className="mb-6">
            <label className="block mb-1 text-left">Password</label>
            <input
              name="password"
              type="password"
              className="w-full px-4 py-2 border rounded"
              value={form.password}
              onChange={handleChange}
              required
            />
          </div>

          <button
            type="submit"
            className="w-full bg-blue-600 text-white py-2 rounder hover:bg-blue-700 transition"
          >
            Login
          </button>

          <div className="flex justify-between mt-4 mb-4 text-sm">
            <Link
              to="/forgot-password"
              className="text-blue-600 hover:underline"
            >
              Forgot password?
            </Link>
            <Link to="/register" className="text-blue-600 hover:underline">
              Register
            </Link>
          </div>
        </form>
        <GoogleLogin />
      </div>
    </div>
  );
}
