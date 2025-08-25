import React, { useState } from "react";
import { useSearchParams, Link, useNavigate } from "react-router-dom";
import api from "../api/axios";

export default function ResetPassword() {
  const [searchParams] = useSearchParams();
  const token = searchParams.get("token");
  const navigate = useNavigate()

  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [message, setMessage] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await api.post("/reset-password", {
        token,
        new_password: newPassword,
        confirm_password: confirmPassword,
      });
      setMessage(res.data.message);
      setTimeout(() => {
        navigate("/")
      }, 3000);
    } catch (error) {
      setMessage(error.response?.data?.detail || "Error resetting password");
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <form
        onSubmit={handleSubmit}
        className="bg-white p-8 rounded shadow max-w-md w-full"
      >
        <h2 className="text-2xl font-bold mb-4">Reset Password</h2>

        <input
          type="password"
          placeholder="New Password"
          className="w-full mb-3 p-2 border rounded"
          value={newPassword}
          onChange={(e) => setNewPassword(e.target.value)}
          required
        />

        <input
          type="password"
          placeholder="Confirm Password"
          className="w-full mb-3 p-2 border rounded"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
          required
        />

        <button className="w-full bg-blue-600 text-white p-2 rounded hover:bg-blue-700">
          Reset Password
        </button>

        {message && (
          <div className="mt-4 text-center">
            <p className="text-sm text-gray-700">{message}</p>
            <Link
              to="/"
              className="mt-2 inline-block text-blue-600 hover:underline"
            >
              Back to Login
            </Link>
          </div>
        )}
      </form>
    </div>
  );
}
