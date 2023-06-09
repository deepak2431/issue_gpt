import React, { useState, ChangeEvent } from "react";
import { useDispatch, useSelector } from "react-redux";
import InputForm from "../components/InputForm";
import Button from "../components/Button";
import {
  addOrg,
  addAccessToken,
  addWebhooksSecret,
  settingsSuccess,
} from "../redux/SettingsReducer";
import { RootState } from "../redux";
import { CONFIG } from "../config";

const SERVER_URL = CONFIG.SERVER_URL;

const Settings = () => {
  const dispatch = useDispatch();

  const [orgName, setOrgName] = useState("");
  const [accessToken, setAccessToken] = useState("");
  const [webhooksSecret, setWebhooksSecret] = useState("");
  const [error, setError] = useState(0);

  const organisation_name = useSelector(
    (state: RootState) => state.settings.orgName
  );
  const access_token = useSelector(
    (state: RootState) => state.settings.accessToken
  );
  const webhooks_secret = useSelector(
    (state: RootState) => state.settings.webhooksSecret
  );
  const settings_saved = useSelector(
    (state: RootState) => state.settings.settingsSaved
  );

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
          dispatch(settingsSuccess(false));
        }
        return response.json();
      })
      .then((resp) => {
        console.log(resp);
        dispatch(settingsSuccess(true));
        dispatch(addOrg(orgName));
        dispatch(addAccessToken(accessToken));
        dispatch(addWebhooksSecret(webhooksSecret));
      });
  };

  return (
    <div className="settings" style={{ margin: "10px" }}>
      {error === 1 && (
        <p style={{ color: "red", margin: "5px" }}>
          Error while saving the settings, Please try again!
        </p>
      )}
      {settings_saved ? (
        <>
          <h3>Your saved settings</h3>
          <div className="saved_settings">
            <h5>Organisation name</h5>
            <p className="settings_saved_info">{organisation_name}</p>
            <h5>Access Token</h5>
            <p className="settings_saved_info">{access_token}</p>
            <h5>Webhooks secret</h5>
            <p className="settings_saved_info">{webhooks_secret}</p>
          </div>
        </>
      ) : (
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
      )}
    </div>
  );
};

export default Settings;
