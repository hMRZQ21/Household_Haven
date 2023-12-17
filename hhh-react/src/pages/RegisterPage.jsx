import React, { useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

function RegisterPage() {
  const auth = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [data, setData] = useState({ name: "", email: "", password: "", street: "", city: "", state: "", zipcode: "", usertype: ""});
  const [error, setError] = useState(false);

  const from = location.state?.from?.pathname || "/";

  const fieldChanged = (name) => {
    return (event) => {
      let { value } = event.target;
      setData((prevData) => ({ ...prevData, [name]: value }));
    };
  };

  const register = async (event) => {
    event.preventDefault();
    let { name, email, password, street, city, state, zipcode, usertype } = data;

    try {
      await auth.register(name, email, password, street, city, state, zipcode, usertype);
      // setRedirectToReferrer(true); // used in react-router v5
      // in react-router v6 navigate changes the pages directly.
      // comment from official docs example:
      //    Send them back to the page they tried to visit when they were
      //    redirected to the login page. Use { replace: true } so we don't create
      //    another entry in the history stack for the login page.  This means that
      //    when they get to the protected page and click the back button, they
      //    won't end up back on the login page, which is also really nice for the
      //    user experience.
      navigate(from, { replace: true });
    } catch (error) {
      setError(true);
    }
  };

  let errorMessage = "";
  if (error) {
    errorMessage = (
      <div className="alert alert-danger" role="alert">
        Registration Failed
      </div>
    );
  }

  return (
    <div className="col-10 col-md-8 col-lg-7">
      <form onSubmit={register}>
        <div className="form-row">
          {errorMessage}
          <input
            type="text"
            className="form-control"
            id="name"
            placeholder="First and Last Name"
            value={data.name}
            onChange={fieldChanged("name")}
            required
          />
          <input
            type="email"
            className="form-control"
            name="email"
            placeholder="Email"
            value={data.email}
            onChange={fieldChanged("email")}
            required
          />
          <input
            type="password"
            className="form-control"
            name="password"
            placeholder="Password"
            value={data.password}
            onChange={fieldChanged("password")}
            required
          />
          <input
            type="text"
            className="form-control"
            name="street"
            placeholder="Street"
            value={data.street}
            onChange={fieldChanged("street")}
            required
          />
          <input
            type="text"
            className="form-control"
            name="city"
            placeholder="City"
            value={data.city}
            onChange={fieldChanged("city")}
            required
          />
          <input
            type="text"
            className="form-control"
            name="state"
            placeholder="State"
            value={data.state}
            onChange={fieldChanged("state")}
            required
          />
          <input
            type="text"
            className="form-control"
            name="zipcode"
            placeholder="Zipcode"
            value={data.zipcode}
            onChange={fieldChanged("zipcode")}
            required
          />
          <input
            type="checkbox"
            className="form-control"
            name="usertype"
            placeholder="Are you a Seller?"
            value={data.usertype}
            onChange={fieldChanged("usertype")}
            required
          />
          <button type="submit" className="btn btn-primary">
            Submit
          </button>
        </div>
      </form>
    </div>
  );
}

export default RegisterPage;