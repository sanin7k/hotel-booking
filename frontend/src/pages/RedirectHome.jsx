import React, { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/axios";

export default function RedirectHome() {
  const navigate = useNavigate();

  useEffect(() => {
    const redirect = async() => {
      const response = await api.get("/logged_in");
      const logged_in = response.data.logged_in
      if (logged_in) {
        navigate("/dashboard");
      } else {
        navigate("/login");
      }
    };

    redirect();
  }, [navigate]);

  return (
    <div className="min-h-screen flex items-center justify-center text-lg text-gray-700">
      Redirecting...
    </div>
  );
}
