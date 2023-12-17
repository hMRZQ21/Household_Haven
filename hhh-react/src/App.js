import { React } from "react";
import { BrowserRouter, Routes, Route, Link, NavLink } from "react-router-dom";

import { AuthProvider } from "./context/AuthContext";
import AuthButton from "./components/AuthButton";
import HomePage from "./pages/HomePage";
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import "./App.css";

function Navigation(props) {
  return (
    <nav className="navbar navbar-expand-sm navbar-dark bg-dark shadow mb-3">
      <div className="container-fluid">
        <Link className="navbar-brand" to="/">
          Household Haven
        </Link>
        <AuthButton />
      </div>
    </nav>
  );
}

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
          <Navigation />
          <div className="container-xl text-center">
            <div className="row justify-content-center">
              <Routes>
                <Route path="/login" element={<LoginPage />} />
                <Route path="/register" element={<RegisterPage />} />
                <Route path="/" element={<HomePage />} />
              </Routes>
            </div>
          </div>
      </BrowserRouter>
    </AuthProvider>
  );
}

// --- Old App.js
// function App() {
//   const [message, setMessage] = useState('');

//   useEffect(() => {
//     fetch('http://127.0.0.1:5000/home')
//       .then(response => response.json())
//       .then(data => setMessage(data.message));
//   }, []);

//   return (
//     <div>
//       <h1>{message}</h1>
//     </div>
//   );
// }

export default App;