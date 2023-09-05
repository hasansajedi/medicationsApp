import React from 'react';
import './Header.css';
import logo from './logo.png';

function Header() {
    return (
        <div className="header">
            <div className="logo">
                <img src={logo} className="App-logo" alt="logo" />
            </div>
            <div className="app-name">Medications</div>
        </div>
    );
}

export default Header;
