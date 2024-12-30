import * as admin from "firebase-admin";
import { onCall, HttpsError } from "firebase-functions/v1/https";

admin.initializeApp();


export const setUserRole = onCall(async (data, context) => {
  if (!context.auth || context.auth.token.role !== 'admin') {
    throw new HttpsError(
      "permission-denied",
      "Only admins can set roles."
    );
  }

  const { uid, role } = data;

  if (!uid || !role) {
    throw new HttpsError(
      "invalid-argument",
      "User ID and role are required."
    );
  }

  try {
    // Set custom claims for the user
    await admin.auth().setCustomUserClaims(uid, { role });
    return { message: `Role '${role}' assigned to user ${uid}` };
  } catch (error) {
    if (error instanceof Error) {
      throw new HttpsError("internal", error.message);
    } else {
      throw new HttpsError("internal", "An unknown error occurred");
    }
  }
});