"use client";
import { supabase } from "@/app/utils/supabaseClient";

const AssignRole = async (userId: string, role: string) => {
  const { error } = await supabase
    .from('user_roles') // or 'auth.users' if using the first option
    .insert([{ user_id: userId, role }]);
    
  if (error) console.error('Error assigning role:', error);
  else console.log('Role assigned successfully');
};
export default AssignRole;