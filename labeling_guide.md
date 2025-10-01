## Guidelines for Email Analysts Conducting Labeling

### **Malicious**
Emails containing phishing, malware, application consent abuse, or otherwise attempts at socially engineering the user to give up credentials, access, or money. Includes extortion, blackmail, callback scams, credential-harvesting links (even if nested in redirections or attachments), and anything delivering malware or suspect executable content. Reconnaissance attacks are also deemed malicious.

#### **Subcategories and Example Scenarios**

1. **Payment Scam (BEC/Invoice Fraud)**
   - **Key Indicators**: 
      - Urgent requests for wire transfers or invoice settlements, often from spoofed executives or vendors.
   - **Typical Tactics**: 
      - Spoofing email especially of a VIP
      - Impersonation of company leadership: impersonate high-level individuals (executives, managers) to request urgent actions like wire transfers or sensitive data, exploiting employees’ trust in leadership.
      - Multiple identity mismatches: Different display name, email domain, and reply-to domain
      - Fake threads 
      - Vendor payment demands
      - Suspicious attachments -- fabircated invoices and W-9 forms
      - Social engineering: Creating fake conversation history to establish legitimacy

2. **Initial Contact BEC (Engagement/Conversation Fraud)**
      - **Definition**: Initial engagement attempts that use minimal business context to establish communication, typically as a first step before more targeted fraud attempts in subsequent messages.
   - **Key Indicators**:
      - Brief messages with minimal context from impersonated senders
      - Attempts to establish communication without specific business details (e.g., check-in, are you in the office)
      - Mismatched sender components: display name, email domain, and reply-to address do not align
      - Urgent requests for alternate contact methods (phone numbers, personal email)
      - Display name matches organizational figure but uses unrelated email domain/address
      - May use Subject lines containing executive names or vague urgent matters without context "URGENT," "PRIORITY," or "IMPORTANT"
      - Suspicious Recipients Pattern: all recipients of the message are the same as the sender.
   - **Typical Tactics**:
      - Impersonation: Employee in the recipient's organization (e.g., organizational or VIP display name)
      - Reply-to manipulation directing responses to attacker-controlled addresses
      - Out-of-band pivoting attempts (asking for cell phone, whatsapp, or personal email details)
      - Social engineering via artificial urgency without specific context
      - Signing with a name different from the email address to create false familiarity
      - Deliberately vague business propositions that require recipient engagement for details
		- Sender email local-part contains a keyword commonly observed in Initial Contact BEC attempts

3. **Advance Fee Fraud (419 Scams)**
   - **Key Indicators**: Promises of large financial rewards that require upfront payment or personal information, often involving inheritance claims, overseas business opportunities, or lottery winnings.
   - **Typical Tactics**:
     - Elaborate stories about trapped funds needing transfer assistance involving impersonation of international organizations or governments
     - Claims of massive inheritance requiring legal fees to release
     - Lottery/prize winning notifications requiring processing fees
     - Overpayment schemes requesting return of excess funds
     - Business proposals requiring initial investment or banking details
     - Humanitarian appeals promising a share of charitable funds

4. **Job Scam (419 Scams)**
   - **Key Indicators**: Unsolicited emails offering lucrative employment opportunities with high pay for minimal qualifications, often claiming affiliation with prestigious organizations (UN, international companies, government agencies). Messages typically contain specific salary details, vague job descriptions, requests for personal information, and communication through non-corporate email channels.

   - **Typical Tactics**:
     - Claims of remote/work-from-home positions
     - Communicates pay in weekly format (e.g., "$700 USD weekly") rather than annual or monthly terms used in legitimate job offers
     - Impersonation of well-known organizations without using official domains
     - Requests to communicate through personal email accounts or messaging apps
     - Directing replies to free email providers (Gmail, Yahoo, Hotmail) despite claiming to represent established organizations
     - Urgent hiring process with minimal screening or qualifications required
     - Requests for personal information (banking details, ID documents, SSN)
     - Initial messages focused on establishing trust before later financial requests
     - Vague information about actual job responsibilities contrasted with very specific payment details

5. **Romance Scams (419 Scams)**
    - **Key Indicators**: Romance/Relationship scams begin with unsolicited messages establishing emotional connection through personal introductions and relationship offers, using compromised legitimate domains while directing replies to free email providers - all tactics designed to build trust before later financial requests.
   - **Typical Tactics**:
      - Unsolicited romantic overtures in a business email context
      - Use of generic relationship-seeking language
      - Requests to continue communication or establish a relationship
      - Reply-to addresses using free email provider
      - May have image attachments (often a picture of the sender) with random filenames
      - Commonly abuses domains that have good reputation, so domain authentication passing does not indicate legitimacy.

6. **Credential Harvesting (Phishing)**
   - **Key Indicators**: Emails urging the user to “verify” or “update” account details, fake file shares that impersonate targeted credentials, suspicious hr/financial document shares
   - **Typical Tactics**:
      - Threats of account suspension
      - Urgent password reset links
      - HTML attachments disguised as secure forms
      - Impersonating fileshare services like Sharepoint or Adobe

7. **Malware Distribution**
   - **Key Indicators**: Suspicious or unexpected attachments (e.g., `.exe`, macro-enabled Office docs, or hidden scripts).
   - **Typical Tactics**: Archiving malicious files (`.zip`, `.rar`), embedding macros in documents, HTML smuggling.

8. **Extortion / Blackmail**
   - **Key Indicators**: Demands for payment (often cryptocurrency) threatening to release private or embarrassing information.
   - **Typical Tactics**: Sextortion emails, claims of hacked webcams or data breaches, personal details to add credibility.

9. **Callback Scam**
   - **Key Indicators**: Callback Phishing is an attempt by an attacker to solicit the victim (recipient) to call a phone number
   Fraudulent invoice/receipt found in the body of the message or as an attachment. Encourages recipients to call a “support line” that is usually a 1-800 variant.
   - **Typical Tactics**: 
      - Fake invoice sent by freemail providers
      - Commonly target the following brands
         - Norton
         - Lifelock
         - McAfee
         - Best Buy/Geek Squad
         - Ebay
         - SecureAnywhere
         - Cryptocurrency purchases
         - Technology purchases like Apple computers/phones
      - Fraudulent phone numbers to “cancel” services
   - **Important Distinctions**:
      - Not all communications containing phone numbers are callback phishing
      - Legitimate business processes often include phone numbers for verification
      - Background checks, employment verification, and financial services legitimately request calls
      - Key differentiator is the urgency, deception, and false pretenses rather than the presence of a phone number

10. **Service Abuse (DocuSign, Dropbox, HelloSign, WeTransfer, DocSend, PandaDoc, etc.)**
   - **Common abused services**: Paypal, Payoneer, DocuSign, Dropbox, Intuit, Google Drive, WeTransfer, Zoho, Zelle, AdobeSign.
   - **Key Indicators**: Notifications appear to come from, or are actually from, legitimate file-sharing/e-sign services but have unusual reply-to domains, suspicious infrastructure (if not legitimate), or suspicious doc names.
   - **Typical Tactics**:
      - The infrastructure that the email is coming from is suspicious and not the official infrastructure of the claimed service
      - IMPORTANT: The **Reply-to address** is an often more accurate representation of the true sender when a legitimate service is used/abused, so data about this address should be taken heavily into account, such as previous communication with the organization. If the reply-to is potentially suspicious while considering Service Abuse, it is likely not benign (recommend verdicting malicious or escalating using unknown verdict if unsure)
      - The **shared link does not match the expected service** (e.g., a Dropbox notification linking to an unrelated domain).
      - The **call-to-action asks for**, credentials, suspicious document shares, financial transactions, or redirects to phishing or malware in some way.
   - **Example Scenarios**:
     - **E-Signature Abuse**: “You have a DocuSign document” or similar from a newly observed reply-to address; doc names referencing urgent financial or human resource matters. Often uses legitimate E-signature infrastructure
     - **Fake E-Signature**: E-Signature Impersonation occurs in message body or attachment and is sent from illegitimate (for example, non-Docusign) infrastructure. Call-to-action asks recipient to click a link to sign documents related financial or human resource matters.
     - **File Share Abuse**: Shared file from “no-reply@dropbox.com” or similar but the domain or link is brand-new; references unknown invoices. Either uses illegitimate infrastructure or Legitimate infrastructure with suspicious reply-to (original sender)
     - **HelloSign Impersonation**: “You have a HelloSign request” but the embedded link leads to credential phishing or malicious attachments.
     - **Trusted Form Abuse**: Misusing legitimate form/survey platforms (Microsoft Customer Voice Forms, Google Forms, SurveyMonkey, etc.) that appear trustworthy but are repurposed for credential harvesting. Often presents the form as a financial or account verification tool rather than its intended survey purpose.
     - **Credential Harvesting & MFA Bypass**
       - Fake "document shared with you" requests leading to credential phishing pages.
       - Calls to "log in" or "authenticate" via fake portals impersonating Microsoft 365, Google, or Dropbox.
       - MFA attacks where victims are tricked into providing verification codes.
       - **Common abused services**: DocuSign, Dropbox, OneDrive, Google Drive, Box, SharePoint.
     - **Financial & Invoice Fraud**
       - Fake invoices, wire transfer requests, or "ACH payment due" shared via legitimate file-sharing platforms.
       - Spoofed finance department names (e.g., "Accounts Payable," "Payroll Admin") in subject lines.
       - Shared documents with misleading names: `"Invoice_Overdue.pdf"`, `"Wire Confirmation.docx"`.
       - **Common abused services**: DocuSign, Dropbox, OneDrive, SharePoint, Payoneer.
     - **HR & Payroll Exploitation**
       - Fake shared files requesting employees to review "Salary Adjustments," "Payroll Reports," or "Benefit Enrollment."  
       - Impersonation of HR representatives or payroll systems.
       - Shared files with document names: `"Employee_Payroll.pdf"`, `"Benefits_Enrollment.docx"`.
       - **Common abused services**: DocuSign, HelloSign, Adobe Sign, Google Drive, OneDrive.
     - **Legal & Compliance Scams**
       - Urgent requests to "review and sign" fake legal agreements or compliance documents.
       - Calls-to-action to sign `"Contract_Agreement.pdf"` or `"Risk_Assessment.docx"`  
       - **Common abused services**: DocuSign, HelloSign, PandaDoc, Adobe Sign
     - **Malware Delivery via File-Sharing Links**
       - Shared file contains malware (e.g., `.zip`, `.js`, `.exe`) disguised as invoices, scanned documents, or reports.
       - "Download before it expires" urgency tactics.
       - **Common abused services**: WeTransfer, Google Drive, Dropbox, MediaFire, Mega.
     - **Callback Scams via Third-Party Services**
       - Fraudulent invoice instructing a call to "resolve a billing issue" or "report not making purchase" culminating in financial theft or malware deployment.
       - Shared document contains a **phone number** to "confirm details" leading to fraud.
       - Often paired with fake invoices, tax documents, or business payment instructions.

   - **Labeling Guidance**:  
     - **Malicious → Service Abuse**: If the email exploits any of these services for phishing, credential theft, or financial fraud.
     - **Unknown**: If the sender or content raises concerns but lacks definitive signs of abuse.
     - **Benign**: Only if the email is a verified legitimate file-sharing request from a known sender.

11. **Reconnaissance**
   - **Key Indicators**: Reconnaissance emails test the waters of an organization's email security defenses, verifying deliverability to intended recipients, confirming the validity of specific email addresses, and assessing the effectiveness of spam filters and other security measures in place.
   - **Typical Tactics**:
      - Large number of recipients that are unknown to the organization OR all recipients are bcc'd, undisclosed recipients, or self-sender pattern.
      - Message body contains no links or attachments.
      - Lack of substantive content: Message body contains no text or an extremely short body.
      - Extremely short, non-descriptive subject
      - Message is from an unknown sender.
      - Legitimate email infrastructure and authentication checks passing can be typically observed.

12. **Additional Malicious Techniques**
   - **Suspicious Mailer from Gmail or Freemail**: Headers show an odd mailer user agent (e.g., “Microsoft CDO for Windows 2000”) but the sender is a generic `@gmail.com` or other freemail.
   - **Adobe Image Lure with Suspicious Link**: Email or PDF uses Adobe logos/images; link redirects to a malicious site.
   - **Adobe Image Lure + QR Code**: Adobe-branded image contains a QR code leading to phishing pages or forced downloads.
   - **HTML Smuggling Attachment**: `.html` file uses JavaScript (`eval`, `atob`, etc.) to auto-download malware.
   - **Callback Phishing via PDF/Image**: Attached invoice or receipt instructs the user to call a number; phone operator pushes RAT installs or fraudulent payments.
   - **Brand Impersonation + Credential Theft**: Message fakes a trusted brand (Microsoft, PayPal, etc.) and threatens account closure unless the user logs in via a suspicious link.
	- **Credential Phishing in Attached EML or message/rfc822 files**
      - **CRITICAL ANALYSIS REQUIRED**: Message attachments require max depth of attachment analysis and deserve increased scrutiny as they can conceal malicious content
		- PRIMARY INDICATORS:
         * Vague reference to attachment in message body
			* ANY brand styling combined with links to unrelated domains (e.g., Microsoft/DocuSign/Adobe/PandaDoc/DocSend Brand Impersonation with non-aligned link domain)
			* Interface mimicry of popular services (file sharing, document signing, etc.)
			* Call-to-action elements (buttons, highlighted links) leading to suspicious domains
			* Unnecessary attachment format for content that could be sent directly
		- VERIFICATION STEPS:
			* Compare ALL visual styling and branding against ALL link destinations
			* Check if sender patterns (self-sender, unusual forwarding, undisclosed recipients) compound suspicion
			* Evaluate whether legitimate business need exists for the attachment format
		- FALSE POSITIVE MITIGATION:
			* Legitimate EML attachments typically preserve important email threads or evidence
			* Expected formatting maintains brand-domain alignment even in attachments
---

### **Spam**
Emails that are unwanted, unsolicited, and typically high volume. They may be borderline scams (e.g., “you’ve won a sweepstake” or "Miracle Health Products") or direct solicitations about things like lead generation, SEO, predatory publishing. Usually lacks a valid unsubscribe mechanism (e.g., hidden or obscured opt-out, or complicated unsubscribe process) and doesn't comply with CAN-SPAM. 

They may also be marketing, adverstising, or bulk emails that, under common sense assumptions, were likeley never opted into by the recepient. Also include Marketing and Bulk email that likely falsely claim or indicate that the recipient opted in or previously communicated with the sender.

#### **Subcategories and Example Scenarios**

1. **High-Volume Bulk Promotions & Item Giveaways**
   - **Key Indicators**: Generic ad blasts with no user consent, Item giveaways "Congrats", "You won" and "Get/Claim your free", and Prize Surveys are common themes.
      - Emails featuring multiple product images arranged in a specific template layout
      - Offers of free products, giveaways, or chances to win prizes by completing surveys
      - Impersonation of popular consumer brands despite not originating from authentic brand domains
      - Attachments embedded in the message or Clickable images leading to external websites for "claiming" prizes or completing surveys (OCR can help surface this)
      - Clickable images leading to external websites for "claiming" prizes or completing surveys 
      - Any other form of high volume bulk or marketing that doesnt comply with CAN-SPAM act

   - **Typical Tactics**: 
      - Promotional content from questionable mailing domains
		  - Subject and/or Display Name contains popular brand + unique tracking identifer
      - Possibly forging or misspelling brand names to bypass filters (e.g., L0WES, C0STC0, DewaIt)
      - Subject Contains misspelling to bypass filters (e.g., WlNNER, FREEBlE, CompIimentary)
      - Generic Product Personalization - Offering items with the recipient's name inserted, a common tactic in bulk marketing spam.
      - Inconsistent Branding - Sender name doesn't align with any elements in the email content or links.
      - Common Product Templates - Multiple similar product offers with just the customer name changed, indicating template-based mass mailing.
      - HTML Comment Stuffing - Large blocks of commented-out HTML containing completely unrelated content (news articles, travel guides, etc.) to artificially increase the ratio of "legitimate" text
      - Gambling Terminology Patterns - Specific terms like "FREE SPINS," "CLAIM," and similar gambling-related offers paired with urgency indicators
      - Multi-language Content Mixing - Combining promotional content with unrelated text in different languages to bypass language-based filtering

2. **Lead Generation/Contact List Solicitation**
   - **Key Indicators**: Unsolicited offers to sell or provide access to contact databases, particularly attendee/user/email lists, decision-maker lists, or professional databases. Often follows up multiple times with "checking in" messages. Unsolicited requests for sponsorship money, especially from unknown conference organizers
   - **Typical Tactics**: Claims of "verified data," "precise targeting," "warm prospects," and "fresh contacts." Uses terminology like "decision makers," "professionals," or "registrants." Frequently mentions specific events or industries while having no real association. Multiple follow-up attempts with phrases like "following up" or "get a chance to review." Promises of "exposure" or other vague benefits

3. **SEO/Website Audit Solicitation**
   - **Key Indicators**: Unsolicited offers for "free website audits" or SEO services, claims about discovering issues with your website ranking.
   - **Typical Tactics**: Generic greetings to "webmaster," promises of "guaranteed first page rankings," claims to have analyzed your site and found problems, offers of comprehensive SEO proposals with unrealistic improvements.

4. **Academic Journal Solicitation**
   - **Key Indicators**: Unsolicited invitations to submit manuscripts or join editorial boards, often mentioning "Impact Factor" or "Special Issues." Frequently emphasizes terms like "peer-review" and "open-access."
   - **Typical Tactics**: Uses academic terminology to appear legitimate, pushes for quick submissions for "upcoming editions," solicits contributions without proper academic context. Often associated with predatory publishing practices.

5. **Miracle Health Product Solicitation**
   - **Key Indicators**: Unsolicited emails promoting "miracle" cures or treatments, often targeting common health concerns like weight loss, hearing loss, or pain. Uses phrases like "no side effects" or claims from "top Harvard doctors."
   - **Typical Tactics**: Makes unrealistic health claims with specific numbers (e.g., "lose X pounds"), promises "easy steps" to cure conditions, references vague "discoveries," and often combines multiple health buzzwords like "miracle," "cure," and specific conditions in a single message.
   
6. **Spam Trying to Masquerade as Graymail**
   - **Key Indicators** Unsolicited marketing emails that falsely imply prior relationship or consent. Uses valid technical elements (unsubscribe links, proper authentication) but contains deceptive practices revealing its unsolicited nature.
   - **Typical Tactics** Has superficial apearance, compliance, and TTPs of Graymail, but contains misleading subject lines (especially "RE:", "FWD:" prefixes with no prior communication), fake reply threads, personalization without prior contact, or false urgency triggers to (falsely) make it seem like communication was opted into or solicited by the recipient.

7. **Unsolicited Financial/Loan Solicitations**
   - **Key Indicators** Unsolicited offers for loans, pre-approval, credit, or financial products with minimal business context; often using personalized greetings to create false familiarity
   - **Typical Tactics**
      - Usually consist of direct questions about borrowing needs/financial situations or claims of pre-approval for loan
      - Content displacement techniques to hide parts of the message
      - Mixing legitimate-appearing disclaimers with suspicious offers
      - Subject lines implying ongoing relationships that don't exist
      - Pre-Approval Language: Phrases like "you've been approved for", "after evaluating your business credit", "REDEEM NOW" without prior application are classic financial spam tactics.
      - "Quick and easy" process promises
      - Use of generic financial terminology in sender names (e.g., Account Manager)
      - Technical authentication that passes checks despite suspicious content
      - Geographic mismatches between sender location (e.g., TLD) and target audience

8. **Unsolicited Vanity Publishing**
   - **Key Indicators** Unsolicited publishing offers that suggest the recipient has expertise or content worthy of publication, often flattering the recipient with personalized title suggestions or claims of being "selected" without having seen their work. These emails typically come from previously unknown senders claiming to be publishers, literary agents, or book development services.
   - **Typical Tactics**
		- Flattery-based engagement: "Your profile/work/expertise would make an excellent book" despite no submission or prior relationship
		- Name-dropping of successful authors or publishers to establish credibility
		- Vague success metrics: "We've helped X authors" or "contributed to Y million books sold"
		- Suggesting specific book titles based on minimal research of the recipient's profile
		- Recently registered domains despite claims of established business history
		- Emphasis on "quick calls" or consultations to discuss publishing opportunities
		- References to the recipient's professional background or LinkedIn profile as qualification for authorship
		- Opt-out mechanisms to appear compliant with anti-spam regulations
9. **Generic Business/Low-Context Commercial Messages**
   - **Key Indicators**: Unsolicited business communications with multiple spam-like delivery methods despite potentially legitimate services.   
   - **Typical Tactics**:
      - **Infrastructure Misalignment**: Using free email providers (Gmail, Yahoo) despite claiming to be established businesses (e.g., "20+ years experience," "industry leader")
      - **Recipient Obscuring**: Sending to "Undisclosed recipients" or using BCC for mass distribution
      - **Filter Evasion**: Placing all substantive content in images or attachments while body contains only generic text/disclaimers
      - **Untargeted Distribution**: No personalization or relevance to recipient's role/industry
      - **Contact Details**: May include legitimate contact information but only in images to bypass text analysis

10. **Get-rich-quick Schemes**:
	- **Key Indicators** Bulk marketing email promoting vague money-making opportunities
	- **Typical Tactics**
		- Urgent subject lines ("Action needed") for marketing content
		- Vague rewards requiring immediate action
		- Artificial account activation without prior relationship

11. **Unsolicited Invites to Dating, Adult Websites**
	- **Key Indicators** Unsolicited emails promoting adult dating sites, pornographic content, or explicit services. Often disguises itself as legitimate services or uses compromised accounts to bypass filters.
	- **Typical Tactics**
		- Promises of meeting local singles/hookups with minimal effort
		- Contains sexually suggestive language or imagery
		- Often abuses legitimate services or platforms to distribute content
		- Uses emoji-heavy subject lines with hearts, kisses, or other suggestive symbols
		- Frequently includes phrases like "join our community," "exclusive access," or "free membership"
		- May impersonate legitimate platforms while directing to suspicious adult-oriented domains
		- Often includes claims about "no credit card required" or "no personal information needed"
		- Uses reply-to addresses on unrelated domains to the claimed sender
		- May contain attachments designed to make the email appear more legitimate

---

### **Graymail**
Legitimate bulk or business-to-business emails that some recipients may want, others may not. Should have been solicited or at least plausibly subscribed to (even if the recipient forgot). Typically has a valid unsubscribe link, one-click-unsubscribe field in headers, or it is sent via bulk mailing infrastructure (which can be identified from `X-` header values). Almost all non-spam bulk emails with valid opt-out methods are graymail.

Some professional cold outreach is considered graymail, but anything that is asking for money (in any form, i.e sponsorship) or asking if you want to be part of a mailing/attendee list for any reason is likeley spam!

#### Technical Tactics (applies across all graymail subtypes):

**Tracking Implementation**
   - Tracking Pixel in HTML body for open rate monitoring
   - Link tracking via redirect platforms
   - Message identifiers: a string of random alpha-numeric characters at the end of the message body (e.g., "caf4944a0h-jY6T-0a4b95d5c-")

**Mass Distribution Infrastructure**
   - Use of bulk sending platforms
   - List management artifacts in headers
   - Unsubscribe mechanisms (legally required)
   - Batch processing indicators

#### **Graymail Themes**

1. **Legitimate Newsletters / Marketing / Mailing Lists**
   - **Key Indicators**: Sent via recognized brands, with permission. Contains valid methods of opting out or unsubscribing.
   - **Typical Tactics**: Regular mailing lists, new product announcements, monthly newsletters.

2. **Opt-In Promotional Campaigns**
   - **Key Indicators**: Prior user subscription or purchase.
   - **Typical Tactics**: Loyalty program offers, store sale events, event reminders.

3. **Professional Cold Outreach**
   - **Key Indicators**: B2B messages about potential partnerships or solutions, perhaps sent 1-many, that offer mutual value.
   - **Typical Tactics**:
      - Unsolicited but not malicious, referencing real industry roles or business problems.
      - Should not be asking for money or being part of attendee/email marketing/mailing/contact lists
      - Vague Reference to Recipient's Work, Relationship-Building Language, Meeting/Call Request Language, and Follow-up Indicators
      - **Tracking identifiers**: Contains unique tracking codes (often alphanumeric strings at message ends like "a1b2c3-xyz") used by marketing automation systems to monitor engagement
      - **Template language patterns**: High density of generic business jargon and buzzwords without specific context (e.g., "strategic alignments," "process improvements," "synergistic opportunities")
      - **Sender communication patterns**: Often shows as regular one-way communication (sender to organization and unsolicited) rather than two-way exchanges - frequent contact from the same sender doesn't automatically make the communication benign
		- **Subject line formatting**: Uses recipient's first name followed by a question (e.g., "Jack, let's have a chat about this opportunity?") or vague positive language to create false familiarity and encourage opening - this pattern is deliberately engineered to increase open rates in bulk email campaigns
   - **Example Scenarios**: 
      - Product demos from established vendors, partnership opportunities from known companies, invitations to established industry events with clear value
      - Unsolicited, but potentially beneficial, requests to meet for demos or zoom calls
      - Regular outreach from sales representatives with minimal personalization but passing authentication
      - Messages showing established sending patterns but containing primarily template-based content

	For B2B cold outreach to qualify as graymail rather than spam, it should meet MOST of these criteria:
		1. Uses proper business domain email matching the company name
		2. Shows evidence of targeting/personalization to recipient's business needs
		3. Content primarily in readable text (not hidden in attachments or images)
		4. Limited use of aggressive marketing tactics (ALL CAPS, excessive punctuation)
		5. Clear, professional presentation consistent with claimed business reputation

Emails failing multiple criteria above should be classified as spam even if offering legitimate services.

4. **Bulk Updates (Political / Nonprofit / Advocacy)**
   - **Key Indicators**: Large-scale mailings to members, donors, or supporters.
   - **Typical Tactics**: Event invitations, policy or fundraising updates, valid unsubscribe, tracking pixels.

---

### **Benign**
Emails that are normal business or personal communications, not malicious, often essential to day-to-day operations. If Suspicious indicators are present it's better to err on the Side of **Unknown**. It's better to be uncertain than to be incorrect.

#### **Subcategories and Example Scenarios**

1. **Routine Business Communications**
   - **Key Indicators**: Known colleagues, vendors, or partners.
   - **Typical Tactics**: Scheduled project updates, everyday conversation threads.

2. **Transactional Notices**
	- **Key Indicators**: Legitimate receipts, invoices, shipping/tracking from recognized services, appointment confirmations with calendar attachments, subscription renewal notifications, upcoming billing reminders.
	- **Typical Tactics**
		- Auto-generated confirmations, renewal notices, subscription reminders
		- Appointment/reservation confirmations with specific date/time details
		- Calendar attachments (.ics files) with matching appointment information
		- Automated booking system notifications from legitimate businesses
		- Service scheduling confirmations from recognized providers

3. **Customer Inquiries / Service / Support Requests**
   - **Key Indicators**: User-initiated queries about an order or account.
   - **Typical Tactics**: 
      - Reference real purchase history, authentic account ID or ticket number.
      - Addressed to the correct support/help email address
      - No suspicious links or attachments
      - Follows expected customer support communication patterns

4. **Personal or Internal Communications**
   - **Key Indicators**: 1:1 or small group messages from internal addresses or personal contacts.
   - **Typical Tactics**: Personal check-ins, shared meeting notes, friendly correspondence.

5. **Legitimate External Communications**
   - **Key Indicators**: External communications from known colleagues, vendors, or partners.
   - **Typical Tactics**: Scheduled project updates, everyday conversation threads, legitimate invoices, receipts.
   - **Example Scenarios**: These are some non-exhaustive list of examples that are considered benign:
      - Legitimate Docusign or third party service requests from known colleagues (checking reply-to domain, etc.)
      - Legitimate invoices from known vendors (checking sender prevelance and history)
      - Legitimate OTP requests from known colleagues (checking reply-to domain, etc.)
      - Welcome, onboarding, or sign up confirmation emails from services opted into by the user (but not the following graymail emails)
      - Sometimes even emails that contain some weak malicious indicators but are overall benign.

6. **Certain One Time Urgent Emails Sent From Bulk or Graymail Infrastructure**
   - **Key Indicators**: Do not contain any malicious indicators, but are security related emails, One Time Passwords, Password Resets, etc. May also be First time welcomes or order confirmations. Meeting requests from calendar or meeting apps that are not malicious, but are sent with bulk infra.
---

### **Unknown**
Emails that contain some indicators that could suggest they are malicious, spam, or graymail but are not enough to make a definitive judgement.

#### **Subcategories and Example Scenarios**

1. **Weak Malicious/Spam/Graymail Indicators**
   - **Key Indicators**: Weak indicators that could suggest the email is malicious, spam, or graymail but are not enough to make a definitive judgement.
   - **Typical Tactics**: External communications from unknown colleagues, vendors, or partners that seem suspicious or out of context, but could be benign.
   - **Example Scenarios**: These are some non-exhaustive list of examples that are considered unknown:
      - Sender does not have a prevelance in the user's organization or history of sending emails to the user, but the email could be from a new vendor or colleague.
      - Sender does not have DMARC setup, but seems like a legitimate sender or message
      - DocuSign that seems suspicious or out of context, but could be legitimate
2. **Conflicting Strong Indicators**
   - **Key Indicators**: Strong indicators exist for multiple categories, but the evidence is not strong enough to justify a definitive judgement.
   - **Example Scenarios**: These are some non-exhaustive list of examples that are considered unknown:
      - Emails that contain strong indicators for both graymail and spam
      - Emails that contain strong indicators for both malicious and spam
      - Emails that are on the border between graymail and benign
      - Not enough evidence exists to make a definitive judgement

--- 


## How to Use These Guidelines
1. **Check the Email Context**: Look at the sender, subject, body content, attachments, and links.
2. **Match Against Key Indicators**: Identify whether it aligns with malicious attributes (phishing, malware, scams), spammy unsolicited marketing, legitimate bulk (graymail), or everyday benign communications.
3. **Label Consistently**: Apply the **Malicious**, **Spam**, **Graymail**, or **Benign** label according to the most fitting category.
4. **When in Doubt**: Label as **Unknown**. Only render a verdict if the email is very clearly one of the categories. If the email is labeled as **Unknown**, it should be reviewed by a senior human analyst, so theres nothing wrong with labeling as **Unknown** if you are not sure. Wheras if you chose the wrong label that is not **Unknown**, there are consequences for the end users based on these types of miscategorizations.