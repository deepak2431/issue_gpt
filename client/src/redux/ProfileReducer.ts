import { createSlice, PayloadAction } from "@reduxjs/toolkit"

export interface profileState {
    orgName: string
    accessToken: string
    webhooksSecret: string
}

const initialState: profileState = {
   orgName: '',
   accessToken: '',
   webhooksSecret: ''
}

export const profileSlice = createSlice({
    name: 'profile',
    initialState,
    reducers: {
        addOrg: (state, action: PayloadAction<string>) => {
            state.orgName = action.payload
        },
        addAccessToken: (state, action: PayloadAction<string>) => {
            state.accessToken = action.payload
        },
        addWebhooksSecret: (state, action: PayloadAction<string>) => {
            state.webhooksSecret = action.payload
        },
    }
})

export const { addOrg, addAccessToken, addWebhooksSecret } = profileSlice.actions
export default profileSlice.reducer