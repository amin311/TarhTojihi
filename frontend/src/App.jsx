import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import ProjectListPage from './pages/ProjectListPage';
import ProjectDetailPage from './pages/ProjectDetailPage';
import LoginPage from './pages/LoginPage';
import HomePage from './pages/HomePage';
import NavBar from './components/NavBar';
import RegisterPage from './pages/RegisterPage';
import NewProjectPage from './pages/NewProjectPage';

function App() {
  return (
    <>
      <NavBar />
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/projects" element={<ProjectListPage />} />
        <Route path="/projects/:id/*" element={<ProjectDetailPage />} />
        <Route path="/projects/new" element={<NewProjectPage />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </>
  );
}

export default App; 