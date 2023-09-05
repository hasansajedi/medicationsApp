import React, {useState, useEffect, useCallback} from 'react';
import './SearchForm.css';
import {searchDrugs} from './DrugsFunctions';
import DrugResults from '../DrugResults/DrugResults';

function SearchForm() {
    const [searchQuery, setSearchQuery] = useState('');
    const [result, setResult] = useState([]);
    const [resultCount, setResultCount] = useState(0);
    const [error, setError] = useState(null);
    const [currentPage, setCurrentPage] = useState(1);
    const [previousPage, setPreviousPage] = useState(1);
    const [loadingMore, setLoadingMore] = useState(false);

    const loadResults = useCallback(async (query, page) => {
            try {
                setLoadingMore(true);
                const response = await searchDrugs(query, page);
                if (response && response.items && response.items.length > 0) {
                    if (response.total >= currentPage * response.size && previousPage < currentPage) {
                        setResult((prevResults) => [...prevResults, ...response.items]);
                        setResultCount(response.total);
                    } else {
                        setResult(response.items);
                        setResultCount(response.total);
                    }
                } else {
                    setResult([]);
                    setResultCount(0);
                }
            } catch (error) {
                console.error(error);
                setError(error);
            } finally {
                setLoadingMore(false);
            }
    }, [currentPage, previousPage]);

    const handleInputChange = (event) => {
        setSearchQuery(event.target.value);
    };

    useEffect(() => {
        const fetchData = async () => {
            // Check if searchQuery is not empty or null before loading results
            if (searchQuery && searchQuery.trim() !== '') {
                await loadResults(searchQuery, currentPage);
            } else {
                // Set results to an empty array if searchQuery is empty or null
                setResult([]);
                setResultCount(0);
            }
        };

        fetchData();
    }, [searchQuery, currentPage, loadResults]);

    const handleLoadMore = () => {
        if (result.length < resultCount && !loadingMore) {
            setPreviousPage(currentPage);
            setCurrentPage((prevPage) => prevPage + 1);
        }
    };

    if (error) return `Error: ${error.message}`;

    return (
        <div>
            <div className="formContainer">
                <h2>Search</h2>
                <div>
                    <input
                        type="text"
                        placeholder="Please enter drug or diseases name..."
                        value={searchQuery}
                        onChange={handleInputChange}
                    />
                </div>
            </div>
            <DrugResults result={result} resultCount={resultCount}/>
            {loadingMore && <p>Loading more results...</p>}
            {result.length < resultCount && (
                <button onClick={handleLoadMore}>Load More</button>
            )}
        </div>
    );
}

export default SearchForm;
