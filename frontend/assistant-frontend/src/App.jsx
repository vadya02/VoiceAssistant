import { Provider } from "mobx-react";
import React from "react";
import { Route, Routes } from "react-router-dom";
import RequireAuth from "./hoc/RequireAuth";
import MainPage from "./pages/MainPage";
import Settings from "./pages/Settings";
import StartPage from "./pages/StartPage";
import store from "./store/Store";
function App() {
	return (
		<div className="App">
			<Provider store={store}>
				<Routes>
					{/* <Route path='/startPage' element={<StartPage Store={AuthStore}/>}/> */}
					<Route path="/StartPage" element={<StartPage store={store} />} />
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
			</Provider>
		</div>
	);
}

export default App;
