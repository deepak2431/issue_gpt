import React from "react";
import "./App.css";

import { Routes, Route, BrowserRouter } from "react-router-dom";

import { Provider } from "react-redux";
import { store, persistor } from "./redux";
import { PersistGate } from "redux-persist/integration/react";
import Dashboard from "./pages/Dashboard";
import Settings from "./pages/Settings";
import Profile from "./pages/Profile";
import Issues from "./pages/Issues";
import Home from "./pages/Home";
import Overview from "./pages/Overview";

const App = () => {
  return (
    <div className="App">
      <Provider store={store}>
        <PersistGate loading={null} persistor={persistor}>
          <BrowserRouter>
            <Routes>
              <Route index element={<Home />} />
              <Route path="/dashboard" element={<Dashboard />}>
                <Route path="overview" element={<Overview />} />
                <Route path="settings" element={<Settings />} />
                <Route path="profile" element={<Profile />} />
                <Route path="issues" element={<Issues />} />
              </Route>
            </Routes>
          </BrowserRouter>
        </PersistGate>
      </Provider>
    </div>
  );
};

export default App;
