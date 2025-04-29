import { observer } from "mobx-react";
import React from 'react';
import { useNavigate } from "react-router";
import Header from '../components/Header';
import StartContent from '../components/StartContent';
import transition from "../transition";
const StartPage = observer(({}) => {
    const navigate = new useNavigate()
    // useEffect(() => {
    //     store.checkAuth().then(() => {if (store.isAuthenticated === true){
    //       navigate('/MainPage')
    //   }})
    //     console.log('isAuthenticated: ' + store.isAuthenticated)
        
    // }, []);

  return (
    <div style={{height: '90vh'}}>
        <Header showBack={false}/>
        <StartContent/>
        {/* <Test/> */}
    </div>
  )
})

export default transition(StartPage) 