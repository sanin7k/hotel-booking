import React, { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import api from "../api/axios";

export default function VerifyEmail() {
  const [searchParams] = useSearchParams();
  const [status, setStatus] = useState("verifying"); // verifying | success | error
  const [message, setMessage] = useState("");

  const token = searchParams.get("token");

  useEffect(() => {
    const verify = async () => {
      try {
        const response = await api.get(`/auth/verify-email?token=${token}`);
        setStatus("success");
        setMessage(response.data.message || "Email verified successfully!");
      } catch (error) {
        setStatus("error");
        setMessage(error.response?.data?.detail || "Verification failed.");
      }
    };

    if (token) verify();
    else {
      setStatus("error");
      setMessage("No token found");
    }
  }, [token]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="bg-white p-8 rounded shadow w-full max-w-md text-center">
        {status === "verifying" && (
          <p className="text-gray-600">Verifying your email...</p>
        )}

        {status === "success" && (
          <>
            <h2 className="text-2xl font-bold text-green-600 mb-4">
              ✅ Verified
            </h2>
            <p className="text-gray-700 mb-4">{message}</p>
            <a href="/" className="text-blue-600 hover:underline">
              Login now
            </a>
          </>
        )}

        {status === "error" && (
          <>
            <h2 className="text-2xl font-bold text-red-600 mb-4">
              ❌ Verification Failed
            </h2>
            <p className="text-gray-700 mb-4">{message}</p>
            <a href="/" className="text-blue-600 hover:underline">
              Back to login
            </a>
          </>
        )}
      </div>
    </div>
  );
}
