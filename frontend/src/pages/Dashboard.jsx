import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/axios";

import LogoutButton from "../components/LogoutButton";

export default function Dashboard() {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const response = await api.get("/auth/profile");
        setUser(response.data);
      } catch (error) {
        console.error("Token expired or invalid", error);
        navigate("/login", { replace: true, state: { expired: true } });
      } finally {
        setLoading(false);
      }
    };

    fetchProfile();
  }, [navigate]);

  if (loading)
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        Loading...
      </div>
    );

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="bg-white p-6 rounded shadow w-full max-w-md">
        <h2 className="text-2xl font-bold mb-2">
          Welcome, {user.display_name}
        </h2>
        <p className="text-gray-600">Username: {user.username}</p>
        <p className="text-gray-600">Email: {user.email}</p>
        <div className="text-sm mt-4 text-center">
          <LogoutButton />
        </div>
      </div>
    </div>
  );
}
