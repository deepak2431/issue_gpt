import React, { useState, ChangeEvent } from "react";
import { useDispatch } from "react-redux";
import InputForm from "../components/InputForm";
import Button from "../components/Button";
import {
  addOrg,
  addAccessToken,
  addWebhooksSecret,
} from "../redux/SettingsReducer";

const SERVER_URL =
  "https://f6b1-2401-4900-3ccc-48d9-d822-62f2-f4cb-d409.ngrok-free.app";

const Settings = () => {
  const dispatch = useDispatch();

  const [orgName, setOrgName] = useState("");
  const [accessToken, setAccessToken] = useState("");
  const [webhooksSecret, setWebhooksSecret] = useState("");
  const [error, setError] = useState(0);
  const [success, setSuccess] = useState(0);

  const handleOrgChange = (e: ChangeEvent<HTMLInputElement>) => {
    setOrgName(e.target.value);
  };
  const handleTokenChange = (e: ChangeEvent<HTMLInputElement>) => {
    setAccessToken(e.target.value);
  };
  const handleSecretChange = (e: ChangeEvent<HTMLInputElement>) => {
    setWebhooksSecret(e.target.value);
  };

  const handleSubmit = () => {
    dispatch(addOrg(orgName));
    dispatch(addAccessToken(accessToken));
    dispatch(addWebhooksSecret(webhooksSecret));

    const requestData = {
      organisation_name: orgName,
      personal_access_token: accessToken,
      webhooks_secret: webhooksSecret,
    };

    const requestOptions = {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(requestData),
    };

    fetch(`${SERVER_URL}/github_keys`, requestOptions)
      .then((response) => {
        if (response.status !== 201) {
          setError(1);
          setSuccess(0);
        }
        return response.json();
      })
      .then((resp) => {
        console.log(resp);
        setSuccess(1);
      });
  };

  return (
    <div className="settings" style={{ margin: "10px" }}>
      {error === 1 && (
        <p style={{ color: "red", margin: "5px" }}>
          Error while saving the settings, Please try again!
        </p>
      )}
      {success === 0 ? (
        <>
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
          <Button text="Submit details" onPress={handleSubmit} />
        </>
      ) : (
        <h2>Settings saved successfully</h2>
      )}
    </div>
  );
};

export default Settings;
