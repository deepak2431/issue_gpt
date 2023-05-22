import { configureStore } from "@reduxjs/toolkit";
import { useDispatch } from "react-redux";

import SettingsReducer from "./SettingsReducer";

export const store = configureStore({
  reducer: {
    settings: SettingsReducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
export const useAppDispatch = () => useDispatch<AppDispatch>();
