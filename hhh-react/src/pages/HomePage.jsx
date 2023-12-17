import React, { useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

function HomePage() {
  const auth = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [error, setError] = useState(false);

  // const from = location.state?.from?.pathname || "/";

  let errorMessage = "";
  if (error) {
    errorMessage = (
      <div className="alert alert-danger" role="alert">
        Login Failed
      </div>
    );
  }

  return (
    <div>
      <header>
        <h1>Household Haven Homepage</h1>
      </header>
      <main>
        <p>Hello {auth.user.name}! Welcome to my simple React home page! This is a basic example of a React project.</p>
        <img src="https://via.placeholder.com/300" alt="Placeholder" />
      </main>
    </div>
  );
}

export default HomePage;