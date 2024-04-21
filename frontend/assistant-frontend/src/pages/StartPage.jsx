import { observer } from "mobx-react";
import React, { useEffect } from 'react';
import { useNavigate } from "react-router";
import Header from '../components/Header';
import StartContent from '../components/StartContent';
import store from "../store/Store";
const StartPage = observer(({}) => {
    const navigate = new useNavigate()
    useEffect(() => {
        store.checkAuth()
        if (store.isAuthenticated === true){
            navigate('/MainPage')
        }
        
    }, []);

  return (
    <div style={{height: '90vh'}}>
        <Header showBack={false}/>
        <StartContent/>
        {console.log(process.env.REACT_APP_URL)}
        {/* <Test/> */}
    </div>
  )
})

export default StartPage