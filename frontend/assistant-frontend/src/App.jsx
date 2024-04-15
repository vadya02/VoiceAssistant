import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import StartPage from './components/StartPage';
import { Provider } from "mobx-react";
import store from './store/Store';

import MainPage from './components/MainPage/MainPage';
import Settings from './components/Settings';
import Dashboard from './components/Dashboard/Dashboard';
function App() {
  return (
    <div className="App">
      <Provider store={store}>
        <Router>
          {/* <Header/> */}
          <Routes>
          {/* <Route path='/startPage' element={<StartPage Store={AuthStore}/>}/> */}
            <Route path='/StartPage' element={<StartPage store={store}/>}/>
            <Route path='/MainPage' element={<MainPage store={store}/>}/>
            <Route path='/Settings' element={<Settings store={store}/>}/>
            <Route path='/Dashboard' element={<Dashboard store={store}/>}/>
          </Routes>
        
        </Router>
      </Provider>
    </div>
  );
}

export default App;
