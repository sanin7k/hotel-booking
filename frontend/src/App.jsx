import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import Login from "./pages/Login";
import Register from "./pages/Register";
import VerifyEmail from "./pages/VerifyEmail";
import ForgotPassword from "./pages/ForgotPassword";
import ResetPassword from "./pages/ResetPassword";
import Dashboard from "./pages/Dashboard";
import RedirectHome from "./pages/RedirectHome";

function App() {
  return (
    <>
      <Router>
        <Routes>
          <Route path="/" element={<RedirectHome />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/verify-email" element={<VerifyEmail />} />
          <Route path="/forgot-password" element={<ForgotPassword />} />
          <Route path="/reset-password" element={<ResetPassword />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="*" element={<div>400 Not Found</div>} />
        </Routes>
      </Router>
    </>
  );
}

export default App;
