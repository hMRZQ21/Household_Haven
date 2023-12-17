import React, { useState, useEffect, createContext } from "react";

const AuthContext = createContext();
const { Provider } = AuthContext;

const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(false);

  useEffect(() => {
    async function checkIfUserIsLoggedIn() {
      try {
        let response = await fetch("/auth/login");

        if (!response.ok) {
          throw new Error("Unauthenticated");
        }

        let fetchedUser = await response.json();
        setUser(fetchedUser);
      } catch (error) {
        setUser(false);
      }
    }

    checkIfUserIsLoggedIn();

    return () => {
      // clean up function
    };
  }, []);

  const login = async (email, password) => {
    let response = await fetch("/auth/login", {
      method: "POST",
      body: JSON.stringify({ email, password }),
      headers: {
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) {
      throw new Error("Login Failed");
    }

    const loggedInUser = await response.json();
    setUser(loggedInUser);

    return loggedInUser;
  };

  const register = async (name, email, password, street, city, state, zipcode, usertype) => {
    let response = await fetch("/auth/register", {
      method: "POST",
      body: JSON.stringify({
        name,
        email,
        password,
        street,
        city,
        state,
        zipcode,
        usertype,
      }),
      headers: {
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) {
      throw new Error("Signup Failed");
    }

    const loggedInUser = await response.json();
    setUser(loggedInUser);

    return loggedInUser;
  };

  const signout = async () => {
    let response = await fetch("/auth/logout", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    });
    if (!response.ok) {
      throw new Error("Logout Failed");
    }

    const body = await response.json();
    setUser(false);

    return body;
  };

  return (
    <Provider
      value={{
        login,
        register,
        signout,
        isAuthenticated: user ? true : false,
        user,
      }}
    >
      {children}
    </Provider>
  );
};

// Create our own hook for accessing the context from any functional component
function useAuth() {
  return React.useContext(AuthContext);
}

export { useAuth, AuthProvider };