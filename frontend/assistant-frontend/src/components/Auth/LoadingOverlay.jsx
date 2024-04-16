// LoadingOverlay.tsx
import React from 'react';
import "./Auth.css";

const LoadingOverlay = ({ show }) => {
    return (

        <div className={`overlay ${show ? 'active' : ''}`}>
            <div className="overlay-content">
                <div className="text-center">
                    <div className="spinner-border" role="status">
                        {/* <span className="visually-hidden">Loading...</span> */}
                    </div>
                </div>
            </div>
        </div>

    )

    // <Modal show={show} keyboard={false} centered >
    //   <Spinner animation="border"></Spinner>
    // </Modal>
}

export default LoadingOverlay;
