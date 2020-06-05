CREATE TABLE [Users] (
	[user_id] VARCHAR(100),
	[username] VARCHAR(20) PRIMARY KEY NOT NULL,
	[displayname] VARCHAR(20)  NULL,
	[pub_key] VARCHAR(100) NOT NULL,
  [credential_id] VARCHAR(100),
  [sign_count] INT,
  [icon_url] VARCHAR(20),
  [rp_id] VARCHAR(20)
);

CREATE TABLE [PublicKeyCredentialCreationOptions] (
    [rp_name] VARCHAR(20),
    [rp_id] VARCHAR(20),
    [user_id] VARCHAR(100) PRIMARY KEY NOT NULL,
    [user_displayname] VARCHAR(20),
    [user_username] VARCHAR(20),
    [challenge] VARCHAR(100)
);
