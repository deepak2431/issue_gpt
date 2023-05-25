import { createSlice, PayloadAction } from "@reduxjs/toolkit";

export interface settingsState {
  orgName: string;
  accessToken: string;
  webhooksSecret: string;
  settingsSaved: boolean;
}

const initialState: settingsState = {
  orgName: "",
  accessToken: "",
  webhooksSecret: "",
  settingsSaved: false,
};

export const settingsSlice = createSlice({
  name: "settings",
  initialState,
  reducers: {
    addOrg: (state, action: PayloadAction<string>) => {
      state.orgName = action.payload;
    },
    addAccessToken: (state, action: PayloadAction<string>) => {
      state.accessToken = action.payload;
    },
    addWebhooksSecret: (state, action: PayloadAction<string>) => {
      state.webhooksSecret = action.payload;
    },
    settingsSuccess: (state, action: PayloadAction<boolean>) => {
      state.settingsSaved = action.payload;
    },
  },
});

export const { addOrg, addAccessToken, addWebhooksSecret, settingsSuccess } =
  settingsSlice.actions;
export default settingsSlice.reducer;
