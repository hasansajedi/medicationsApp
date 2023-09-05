import React from 'react';
import './DrugResults.css'

function capitalizeFirstLetter(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
}

function DrugResults({result, resultCount}) {
    return (
        <div className="resultsContainer">
            {result.length > 0 && (
                <h5>Showing {resultCount} results</h5>
            )}
            {result.length > 0 && (
                <div className="cardContainer">
                    {result.map((drug) => (
                        <div key={drug.id} className="card">
                            <div className="cardHeader">
                                <div className="leftHeader">
                                    <h4>{drug.name}</h4>
                                </div>
                                <div className="rightHeader">
                                    <p>Released on: <b>{drug.released}</b></p>
                                </div>
                            </div>
                            <div className="cardBody">
                                <p className="diseases">{drug.diseases.map(capitalizeFirstLetter).join(' - ')}</p>
                                <hr/>
                                <p className="description">{drug.description}</p>
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}

export default DrugResults;