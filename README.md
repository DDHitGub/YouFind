# YouFind - Dive into Data

## Latest version (complete package) is in main.

- Documentation for Backend (for AutoConverter) is in folder AutoConverter.
  
- Developer documentation and User documentation are in folder documentations. 
 
- For the e-mail-verification-function you have to set up the config.ini in folder email-verify-branch.
  - Since our VuFind runs on a local server, it could not send real emails to users.
  - To test it, you have to install a tool that emulates emails locally.
  - For this we used Mailhog: you can set config.ini to localhost:8025 and type in any email to test it.
  - In folder email-verify-branch is mailhog for windows users, if you want mailhog for linux/mac please visit
    the official mailhog repository https://github.com/mailhog/MailHog.
