import React from 'react';
import Sidebar from './Sidebar';
import '../styles/Layout.css';

function Layout({ children }) {
  return (
    <div className="app-layout">
      <Sidebar />
      <main className="main-content">
        {children}
      </main>
    </div>
  );
}

export default Layout;