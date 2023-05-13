import { configureStore } from "@reduxjs/toolkit";
import { useDispatch } from "react-redux";

import ProfileReducer from "./ProfileReducer";

export const store = configureStore({
    reducer: {
        profile: ProfileReducer,
    }
})

export type RootState = ReturnType<typeof store.getState>
export type AppDispatch = typeof store.dispatch
export const useAppDispatch = () => useDispatch<AppDispatch>()