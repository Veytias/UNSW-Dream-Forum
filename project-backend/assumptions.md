Project assumption


    For Auth:       
    1. assume the auth_user_id and u_id are unique and will always be a positive number, and user id start at 1. e.g. if Emma is the 6th registered.user, her u_id would be 6
    
    2. assume one user won't login twice, that is, user would not try login when he/she has already logged in.

    3. assume auth_user_id is same as current user's u_id.
    
    4. assume user automatically login when register, returning a token for that session.

    5. assume program will check token validity in auth_logout automatically.

    6. assume data will be stord at database.p persistently.




    For Channel:

   1. Assume channel_id is unique and will always be a positive number, and it start at 1.

   2. Assume channel_name does not need to be unique.

   3. Assume the creater of channel will become the member and owner of this channel automatically.

   4. Assume inviter never invite invitee into the same channel more than once.

   5. Assume inviter need to login first to invite someone else.

   6. Assume user need to login first to join channels.

   7. Assume joiner never join the same channel more than once.

   8. Assume user need to login first to list channels.

   9. Assume channels_list and channels_listall only return channel_id and channel_name.

   10. Assume the new onwer of the channel is already a member if they did not in this channel.


    For Messages:
   1. Assume message_id is unique and will always be a positive number, and it start at 1.

   2. Assume each message should contain the message_id, channel_id/dm_id, user_id, message_content, time_created.

   3. Assume message_edit/remove work for messages in both dms and channels.

   4. Assume search function will search for the message that contains the query_str as a substring.

   5. Assume 

    For DM:
   1. Assume dm_id is unique and will always be a positive number, and it start at 1.

   2. Assume each dm must have at least two different users.

   3. Assume the creater of DM will become the member and owner of this DM automatically.

    For User:
   1. Assume user must login to modify their information.

   2. Assume the users' default photo is 'initial.jpg'

    For Admin:
   1. Assume user must login first to operate.

    For StandUp:
   1. Assume the user is already the member of given channel. 











    


   





