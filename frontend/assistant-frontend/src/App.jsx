import { AnimatePresence } from "framer-motion";
import { Provider, observer } from "mobx-react";
import React, { useEffect } from "react";
import { useNavigate } from "react-router";
import { Route, Routes, useLocation } from "react-router-dom";
import RequireAuth from "./hoc/RequireAuth";
import History from "./pages/History";
import MainPage from "./pages/MainPage";
import Settings from "./pages/Settings";
import StartPage from "./pages/StartPage";
import store from "./store/Store";


const App = observer(() =>  {

	const navigate = useNavigate()
	const location = useLocation();
  useEffect(() => {
		store.checkAuth().then(() => {if (store.isAuthenticated === false){
			navigate('/')
	} else {
		navigate('/MainPage')
	}})
		console.log('isAuthenticated: ' + store.isAuthenticated)
		
	}, []);
	return (
		<div className="App">
			<Provider store={store}>
          <AnimatePresence mode="wait">
          <Routes location={location} key={location.pathname}>
							<Route index path="/" element={<StartPage store={store} />} />
							<Route index path="/history" element={<History store={store} />} />
							<Route
								path="/MainPage"
								element={
									<RequireAuth>
										<MainPage store={store} />
									</RequireAuth>
								}
							/>
							<Route path="/Settings" element={<Settings store={store} />} />
						</Routes>
          </AnimatePresence>
						

			</Provider>
		</div>
	);
})

export default App;
