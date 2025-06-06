import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '@/context/AuthContext';

function NavBar() {
  const { token, logout } = useAuth();
  return (
    <nav className="navbar navbar-expand-lg navbar-light bg-light mb-4">
      <div className="container">
        <Link className="navbar-brand fw-bold" to="/">طرح توجیهی</Link>
        <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navMenu">
          <span className="navbar-toggler-icon"></span>
        </button>
        <div className="collapse navbar-collapse" id="navMenu">
          <ul className="navbar-nav ms-auto mb-2 mb-lg-0">
            <li className="nav-item">
              <Link className="nav-link" to="/projects">پروژه‌ها</Link>
            </li>
            {token ? (
              <li className="nav-item">
                <button className="btn btn-outline-danger" onClick={logout}>خروج</button>
              </li>
            ) : (
              <li className="nav-item">
                <Link className="btn btn-outline-primary" to="/login">ورود / ثبت‌نام</Link>
              </li>
            )}
          </ul>
        </div>
      </div>
    </nav>
  );
}

export default NavBar; 