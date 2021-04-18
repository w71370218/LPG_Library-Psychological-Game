const { CognitoIdentityClient } = require("@aws-sdk/client-cognito-identity");
const {
  fromCognitoIdentityPool,
} = require("@aws-sdk/credential-provider-cognito-identity");
const { Polly } = require("@aws-sdk/client-polly");
const { getSynthesizeSpeechUrl } = require("@aws-sdk/polly-request-presigner");

// Create the Polly service client, assigning your credentials
const client = new Polly({
  region: "REGION",
  credentials: fromCognitoIdentityPool({
    client: new CognitoIdentityClient({ region: "REGION" }),
    identityPoolId: "IDENTITY_POOL_ID" // IDENTITY_POOL_ID
  }),
});
// Set the parameters
const speechParams = {
  OutputFormat: "OUTPUT_FORMAT", // For example, 'mp3'
  SampleRate: "SAMPLE_RATE", // For example, '16000
  Text: "", // The 'speakText' function supplies this value
  TextType: "TEXT_TYPE", // For example, "text"
  VoiceId: "POLLY_VOICE" // For example, "Matthew"
};