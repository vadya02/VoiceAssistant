// LoadingOverlay.tsx
import React from 'react';
import { Modal, Spinner, Overlay } from 'react-bootstrap';
import "./Auth.css"
interface LoadingOverlayProps {
    show: boolean;
}

const LoadingOverlay: React.FC<LoadingOverlayProps> = ({ show }) => {
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
    ///* <Modal.Body className="text-center" style={{backgroundColor: 'transparent'}}>

    // <Spinner animation="border">

    //  </Spinner>
    //  <p>Loading...</p>

    // </Modal.Body> */}
    //   <Spinner animation="border"></Spinner>
    // </Modal>
}

export default LoadingOverlay;
