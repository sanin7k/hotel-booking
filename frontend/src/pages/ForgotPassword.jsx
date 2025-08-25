import React, { useState } from "react";
import api from "../api/axios";
import { useNavigate } from "react-router-dom";

export default function ForgotPassword() {
  const navigate = useNavigate()
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await api.post("/forgot-password", { email });
      setMessage(response.data.message);
      setTimeout(() => {
        navigate("/")
      }, 3000);

    } catch (error) {
      setMessage(error.response?.data?.detail || "Something went wrong.");
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <form
        onSubmit={handleSubmit}
        className="bg-white p-8 rounded shadow max-w-md w-full"
      >
        <h2 className="text-2xl font-bold mb-4">Forgot Password</h2>
        <input
          type="email"
          placeholder="Enter your email"
          className="w-full mb-4 p-2 border rounded"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <button className="w-full bg-blue-600 text-white p-2 rounded hover:bg-blue-700">
          Send Reset Link
        </button>
        {message && <p className="mt-4 text-sm text-gray-700">{message}</p>}
      </form>
    </div>
  );
}
