import React, {useEffect} from 'react';
import {BrowserRouter as Router, Route, Routes} from 'react-router-dom';
import SearchDrugForm from './components/SearchForm/SearchForm';
import Header from './components/Header/Header';
import getAccessToken from './context/Auth';
import './App.css';

function App() {
    useEffect(() => {
        getAccessToken()
            .then((newAccessToken) => {
                localStorage.setItem('access_token', newAccessToken);
            })
            .catch((error) => {
                console.error('Access Token Error:', error);
            });
    }, []);

    return (
        <Router>
            <div className="App">
                <Header/>
                <Routes>
                    <Route path="/" element={<SearchDrugForm/>}/>
                </Routes>
            </div>
        </Router>
    );
}

export default App;
