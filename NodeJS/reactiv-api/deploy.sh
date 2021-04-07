GOOGLE_PROJECT_ID=reactiv-309904 # YOUR GCP PROJECT ID GOES HERE
CLOUD_RUN_SERVICE=reactiv-service # NAME OF YOUR CLOUD RUN SERVICE
INSTANCE_CONNECTION_NAME=reactiv-309904:us-central1:reactiv-mysql # PROJECT:REGION:INSTANCE
DB_USER=root # SQL USER 
DB_PASS=root # SQL PASSWORD (DEVELOPMENT ONLY!)
DB_NAME=db_reactiv # DATABASE NAME
PORT=8080

gcloud builds submit --tag gcr.io/$GOOGLE_PROJECT_ID/$CLOUD_RUN_SERVICE \
  --project=$GOOGLE_PROJECT_ID

gcloud run deploy $CLOUD_RUN_SERVICE \
  --image gcr.io/$GOOGLE_PROJECT_ID/$CLOUD_RUN_SERVICE \
  --port=8080 \
  --add-cloudsql-instances $INSTANCE_CONNECTION_NAME \
  --update-env-vars INSTANCE_CONNECTION_NAME=$INSTANCE_CONNECTION_NAME,DB_PASS=$DB_PASS,DB_USER=$DB_USER,DB_NAME=$DB_NAME \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --project=$GOOGLE_PROJECT_ID