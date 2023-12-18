import React from "react";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const AuthButton = () => {
  const auth = useAuth();
  const navigate = useNavigate();

  if (!auth.isAuthenticated) {
    return (
      <div className="btn-group">
        <Link className="btn btn-primary m-1" to="/login">
          Login
        </Link>
        <Link className="btn btn-primary m-1" to="/register">
          Register
        </Link>
      </div>
    );
  }

  const logout = () => {
    auth.logout().then(() => navigate("/"));
  };

  return (
    <div className="text-white">
      Welcome! {auth.user.name}
      <button className="btn btn-primary m-1" onClick={logout}>
        Logout
      </button>
    </div>
  );
};

export default AuthButton;