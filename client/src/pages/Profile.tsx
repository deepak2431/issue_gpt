import React, { useState, ChangeEvent } from "react";
import { useDispatch } from "react-redux";
import InputForm from "../components/InputForm";
import Button from "../components/Button";
import { addOrg, addAccessToken, addWebhooksSecret } from "../redux/ProfileReducer";

const Profile  = () => {

    const dispatch = useDispatch();

    const [orgName, setOrgName] = useState('');
    const [accessToken, setAccessToken] = useState('');
    const [webhooksSecret, setWebhooksSecret] = useState('');

    const handleOrgChange = (e:ChangeEvent<HTMLInputElement>) => {
       setOrgName(e.target.value)
    }
    const handleTokenChange = (e:ChangeEvent<HTMLInputElement>) => {
        setAccessToken(e.target.value)

    }
    const handleSecretChange = (e:ChangeEvent<HTMLInputElement>) => {
        setWebhooksSecret(e.target.value)

    }
    const handleSubmit = () => {

        dispatch(addOrg(orgName))
        dispatch(addAccessToken(accessToken))
        dispatch(addWebhooksSecret(webhooksSecret))

        console.log(
            {
                orgName: orgName,
                accessToken: accessToken,
                webhooksSecret: webhooksSecret
            }
        )
    }

    return(
        <div className="profile">
            <InputForm 
            type="text" 
            id="orgName"
            labelName="Organization Name"
            value={orgName}
            onInputChange={handleOrgChange}
            />
            <InputForm 
            type="password" 
            id="accessToken"
            labelName="Personal Access Token"
            value={accessToken}
            onInputChange={handleTokenChange}
            />
            <InputForm 
            type="password" 
            id="webhooksSecret"
            labelName="Webhooks secret"
            value={webhooksSecret}
            onInputChange={handleSecretChange}
            />
            <Button 
            text="Submit details"
            onPress={handleSubmit}
             />
        </div>
    )
}

export default Profile;