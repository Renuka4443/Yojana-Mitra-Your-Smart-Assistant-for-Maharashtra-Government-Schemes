"""
Question Answering Logic Module
Handles query processing, LLM prompting, and response generation
"""

import google.generativeai as genai
from typing import List, Dict, Optional
import os
from dotenv import load_dotenv


# Load environment variables
load_dotenv()


class QASystem:
    """Manages question answering using Google Gemini API"""
    
    def __init__(self, api_key: str):
        """
        Initialize the QA System
        
        Args:
            api_key: Google Gemini API key
        """
        self.api_key = api_key
        genai.configure(api_key=api_key)
        # Use gemini-2.5-flash for better availability, fallback to gemini-pro if needed
        try:
            self.model = genai.GenerativeModel('gemini-2.5-flash')
        except Exception as e:
            print(f"Warning: Could not load gemini-2.5-flash, trying gemini-pro: {e}")
            try:
                self.model = genai.GenerativeModel('gemini-pro')
            except Exception as e2:
                print(f"Error: Could not load gemini-pro: {e2}")
                raise Exception(f"Failed to initialize Gemini model. Please check your API key. Error: {e2}")
    
    def _create_prompt(self, query: str, retrieved_schemes: List[Dict]) -> str:
        """
        Create a prompt for the LLM based on query and retrieved schemes
        
        Args:
            query: User's question
            retrieved_schemes: List of relevant scheme dictionaries from vector search
            
        Returns:
            Formatted prompt string
        """
        # Prepare scheme context and extract Online/Offline from Application Process
        import re
        scheme_context = ""
        application_process_modes = {}  # Store Online/Offline for each scheme
        
        for i, scheme in enumerate(retrieved_schemes, 1):
            app_process = scheme.get('Application Process', 'N/A')
            
            # Extract Online/Offline from Application Process data
            mode = None
            if app_process and app_process != 'N/A':
                # Check for "Online" or "Offline" at the start or as standalone word
                match = re.search(r'\b(Online|Offline)\b', app_process, re.IGNORECASE)
                if match:
                    mode = match.group(1)  # Get "Online" or "Offline" (preserve case)
                    application_process_modes[i] = mode
            
            scheme_context += f"\n\nScheme {i}:\n"
            scheme_context += f"🌐 Scheme Name: {scheme.get('Scheme Name', 'N/A')}\n"
            scheme_context += f"📋 Details: {scheme.get('Details', 'N/A')}\n"
            scheme_context += f"💰 Benefits: {scheme.get('Benefits', 'N/A')}\n"
            scheme_context += f"✅ Eligibility: {scheme.get('Eligibility', 'N/A')}\n"
            scheme_context += f"📝 Application Process: {app_process}\n"
            scheme_context += f"📄 Documents Required: {scheme.get('Documents Required', 'N/A')}"
        
        # Detect if query is asking about specific information
        query_lower = query.lower()
        
        # Comprehensive eligibility keywords
        eligibility_keywords = [
            'eligibility', 'eligible', 'qualify', 'qualification', 'qualifications', 
            'requirements', 'requirement', 'criteria', 'criterion', 'who can apply',
            'who is eligible', 'who can get', 'qualifying', 'prerequisites', 'prerequisite',
            'conditions', 'condition', 'who qualifies', 'who is qualified',
            'applicable to', 'for whom', 'who is entitled', 'entitlement',
            'need to be', 'must be', 'should be', 'age limit', 'income limit'
        ]
        is_eligibility_query = any(word in query_lower for word in eligibility_keywords)
        
        # Comprehensive application keywords
        application_keywords = [
            'how to apply', 'apply', 'application', 'applications', 'apply for',
            'process', 'procedure', 'steps', 'step', 'method', 'way to apply',
            'application process', 'application procedure', 'how can i apply',
            'how do i apply', 'how can apply', 'how to get', 'how to obtain',
            'apply online', 'apply offline', 'registration', 'register',
            'application form', 'form', 'procedure to apply', 'process to apply',
            'steps to apply', 'application steps', 'apply kese kare',
            'apply kaise kare', 'how to register', 'where to apply'
        ]
        is_application_query = any(word in query_lower for word in application_keywords)
        
        # Comprehensive benefits keywords
        benefits_keywords = [
            'benefit', 'benefits', 'what do i get', 'what do you get', 'what will i get',
            'what will you get', 'what can i get', 'what can you get', 'what is provided',
            'what is given', 'money', 'amount', 'financial assistance', 'financial aid',
            'subsidy', 'subsidies', 'grant', 'grants', 'loan', 'loans', 'pension',
            'scholarship', 'scholarships', 'assistance', 'aid', 'help', 'support',
            'funding', 'fund', 'payment', 'payments', 'reimbursement', 'allowance',
            'compensation', 'incentive', 'incentives', 'cash', 'amount given',
            'what amount', 'how much', 'rupees', 'rs.', '₹', 'rupee'
        ]
        is_benefits_query = any(word in query_lower for word in benefits_keywords)
        
        # Documents keywords
        documents_keywords = [
            'documents', 'document', 'papers', 'paper', 'required documents',
            'needed documents', 'what documents', 'which documents', 'documents needed',
            'documents required', 'required papers', 'needed papers', 'what papers',
            'documents list', 'list of documents', 'documents to submit',
            'submit documents', 'certificate', 'certificates', 'proof', 'proofs',
            'id', 'identity', 'address proof', 'age proof', 'income proof'
        ]
        is_documents_query = any(word in query_lower for word in documents_keywords)
        
        # Detect if query is asking about a scheme in general (not specific section)
        general_scheme_keywords = ["tell me about", "information about", "details about", "about the scheme", "about", "what is", "what's"]
        is_general_scheme_query = any(keyword in query_lower for keyword in general_scheme_keywords) and not (
            is_eligibility_query or is_application_query or is_benefits_query or is_documents_query
        )
        
        prompt = f"""You are a helpful AI assistant specializing in Maharashtra Government Schemes.

User's Question: {query}

Below is information about relevant government schemes from the database:

{scheme_context}

Instructions:
1. Answer the user's question based ONLY on the information provided above
2. Do NOT make up any information or add details not present in the data
3. CRITICAL: Scheme names in the database may include "(Maharashtra)" or other variations. Match schemes based on the core name:
   - "Mahila Samridhi Yojana" matches "Mahila Samridhi Yojana (Maharashtra)"
   - "Indira Gandhi National Widow Pension Scheme" matches "Indira Gandhi National Widow Pension Scheme (Maharashtra)"
   - Look for the main scheme name words and ignore location suffixes
4. If the user asks about a specific scheme by name, find the best matching scheme from the provided data by matching the core scheme name
5. If the user asks about eligibility specifically, extract and provide ONLY the eligibility section from the relevant scheme(s)
6. If the user asks "how to apply" or about application process, extract and provide ONLY the application process section from the relevant scheme(s)
7. If the user asks about benefits or financial assistance, extract and provide ONLY the benefits section from the relevant scheme(s)
8. If the user asks about required documents or papers, extract and provide ONLY the documents required section from the relevant scheme(s)
9. If the user asks for specific information (like "eligibility", "application process", "benefits", "documents"), provide ONLY that section clearly
10. If the user asks for general information about a scheme, provide all sections WITH a brief introduction first
11. Format your answer clearly with headings and bullet points where appropriate
12. IMPORTANT: If a scheme name in the data is similar to the user's query (even if it has "(Maharashtra)" appended), use that scheme's information
13. Use emojis from the scheme data if present (🌐 📋 💰 ✅ 📝 📄)
14. Keep your answer concise and structured
15. CRITICAL: For general scheme queries (like "Tell me about [Scheme Name]"), you MUST start with a 2-3 sentence introduction explaining what the scheme is, who it benefits, and its main purpose. This introduction MUST appear immediately after the scheme name heading, BEFORE any section labels.

CRITICAL FORMATTING RULES - You MUST follow these exactly:
1. Use CLEAN MARKDOWN formatting with proper structure:
   - IMPORTANT: Use ### (h3) for scheme name headings ONLY when providing general information about a scheme (all sections)
   - CRITICAL: For general scheme queries, AFTER the scheme name heading, you MUST write a brief 2-3 sentence introduction explaining what the scheme is, who it's for, and its main purpose. This introduction should be in simple, clear language that anyone can understand.
   - For specific queries (eligibility, application process, benefits, documents), DO NOT use big heading (###) for scheme name
   - For specific queries, you can mention scheme name inline in intro: "To apply for the [Scheme Name]..." or just show the section directly
   - Use **bold** for section labels WITHOUT colon: **📋 Details**, **💰 Benefits**, **✅ Eligibility**, **📝 Application Process**, **📄 Documents Required** (NO COLON after section labels)
   - Use bullet points (-) for lists, with proper indentation
   - Add blank lines between sections for readability
   - Keep text clean and professional

2. Format for general information (all sections):
   ### 🌐 Scheme Name: [Name Here]
   
   [MANDATORY: Start with a brief 2-3 sentence introduction explaining what the scheme is, who it's for, and its main purpose. Write this in simple, clear language. This MUST appear BEFORE the **📋 Details** section label.]
   
   **📋 Details** 
   [Full details content here with proper line breaks]
   
   **💰 Benefits**
   - Benefit 1
   - Benefit 2
   
   **✅ Eligibility**
   - Requirement 1
   - Requirement 2

3. Format for specific queries (eligibility, application, benefits, documents):
   Start with brief intro mentioning scheme name: "To apply for the [Scheme Name]..." or "For [Scheme Name] eligibility..."
   
   **📝 Application Process** (or other section)
   - Step 1
   - Step 2
   
   IMPORTANT: If the Application Process data contains "Online" or "Offline", format the heading as: **📝 Application Process (Online)** or **📝 Application Process (Offline)** (with the mode in brackets). Do NOT include "Online" or "Offline" as a separate line after the heading - it should be part of the heading itself.
   
   CRITICAL FOR LINKS: If the Application Process data contains a URL (like https://mahadbt.maharashtra.gov.in/), display it at the END of the Application Process section as a separate line: "Link: [URL]". The link should be displayed as clickable markdown: "Link: [URL](URL)" or just "Link: URL" if markdown links aren't needed.
   
   DO NOT use ## heading for scheme name in specific queries

4. CRITICAL FORMATTING RULES for section labels:
   - Section labels MUST be on their own line, NEVER on the same line as bullet points
   - CRITICAL: Section labels MUST NOT have any colon (:) at all
   - Correct format: **📋 Details** or **💰 Benefits** or **✅ Eligibility** (NO COLON)
   - WRONG format: **📋 Details:** or **💰 Benefits:** or **✅ Eligibility:** (WITH COLON - DO NOT USE)
   - If the source data already starts with a dash/bullet (-), keep it as-is
   - For example, if the data says "✅ Eligibility: - The farmer should hold...", format it as:
     **✅ Eligibility**
     - The farmer should hold...
   - DO NOT format as: **✅ Eligibility** - Point 1 (WRONG - same line)
   - DO format as: **✅ Eligibility** (on one line) followed by blank line, then - Point 1 (on next line)
   - DO NOT create an empty bullet point after the section label. The first bullet point should contain the actual content.
   - NEVER use any colon (:) in section labels. Use format: **📄 Documents Required** (no colon)

5. IMPORTANT: Only respond with "I don't have that information right now" if ALL of the following are true:
    - None of the provided schemes have names that match or are similar to the user's query
    - The information in ALL provided schemes is completely unrelated to the user's question
    - You have carefully checked all schemes and confirmed none contain relevant information
   Otherwise, try your best to answer using the provided scheme information, even if it's not a perfect match.

{"CRITICAL: The user is specifically asking about eligibility. You MUST find the matching scheme and provide its eligibility information clearly. Match scheme names by their core words, ignoring location suffixes like '(Maharashtra)'. DO NOT use ## heading for scheme name. Start with brief intro mentioning scheme name inline, then show: **✅ Eligibility** (NO COLON - on its own line, NEVER on same line as bullet points), followed by blank line, then bullet points on next line. Only say 'no information' if NO scheme has eligibility data." if is_eligibility_query else ""}

{"CRITICAL: The user is asking how to apply or about the application process. You MUST find the matching scheme and provide its application process information clearly. Match scheme names by their core words (e.g., 'Mahila Samridhi Yojana' matches 'Mahila Samridhi Yojana (Maharashtra)'). Extract the Application Process section from the matching scheme. DO NOT use ## heading for scheme name. Start with brief intro like 'To apply for the [Scheme Name]...' or mention scheme name inline, then show: **📝 Application Process** (NO COLON - on its own line), followed by blank line, then bullet points. IMPORTANT: If the Application Process data contains a URL (like https://mahadbt.maharashtra.gov.in/), display it at the END of the Application Process section as a separate line: 'Link: [URL]'. Only say 'no information' if NO scheme has application process data." + (" IMPORTANT: If the Application Process data contains 'Online' or 'Offline', format the heading as: **📝 Application Process (Online)** or **📝 Application Process (Offline)** (with the mode in brackets). Do NOT include 'Online' or 'Offline' as a separate line after the heading - it should be part of the heading itself." if application_process_modes else "") if is_application_query else ""}

{"CRITICAL: The user is asking about benefits or financial assistance. You MUST find the matching scheme and provide its benefits information clearly. Match scheme names by their core words. Extract the Benefits section from the matching scheme. DO NOT use ## heading for scheme name. Start with brief intro mentioning scheme name inline, then show: **💰 Benefits** (NO COLON - on its own line, NEVER on same line as bullet points), followed by blank line, then bullet points on next line. Only say 'no information' if NO scheme has benefits data." if is_benefits_query else ""}

{"CRITICAL: The user is asking about required documents. You MUST find the matching scheme and provide its documents required information clearly. Match scheme names by their core words. Extract the Documents Required section from the matching scheme. DO NOT use ## heading for scheme name. Start with brief intro mentioning scheme name inline, then show: **📄 Documents Required** (NO COLON - on its own line, NEVER on same line as bullet points), followed by blank line, then bullet points on next line. Only say 'no information' if NO scheme has documents information." if is_documents_query else ""}

{"CRITICAL: The user is asking for general information about a scheme (like 'Tell me about [Scheme Name]'). You MUST follow this EXACT format: 1) Start with a brief 2-3 sentence introduction IMMEDIATELY after the scheme name heading, explaining what the scheme is and its main purpose in simple, clear language. This brief introduction should be the FIRST thing users see after the scheme name. 2) Format MUST be: ### 🌐 Scheme Name: [Name Here] [Brief Introduction: 2-3 sentences explaining what the scheme is, who it's for, and its main purpose. Write this in simple, clear language that anyone can understand.] **📋 Details** [Full details content here] **💰 Benefits** ... **✅ Eligibility** ... **📝 Application Process** ... **📄 Documents Required** ... 3) The brief introduction MUST appear BEFORE the **📋 Details** section label. It should be a standalone paragraph right after the scheme name heading. 4) Example: ### 🌐 Scheme Name: Grant In Aid To Old Age Home This scheme provides financial grants to registered NGOs to support old age homes that offer free lodging, boarding, food, accommodation, and medical assistance to elderly residents. The scheme aims to ensure destitute and disabled elderly persons in Maharashtra receive proper care and support through recognized NGOs. **📋 Details** [Full details...] DO NOT skip the brief introduction. It is MANDATORY for general scheme queries." if is_general_scheme_query else ""}

Now answer the user's question with CLEAN, WELL-FORMATTED markdown:"""
        
        return prompt
    
    def _check_no_info(self, response: str, query: str) -> bool:
        """
        Check if the response indicates no information is available
        
        Args:
            response: LLM response
            query: Original user query
            
        Returns:
            True if response indicates no info available
        """
        no_info_phrases = [
            "don't have that information",
            "don't have information",
            "not available",
            "cannot find",
            "unable to find"
        ]
        response_lower = response.lower()
        return any(phrase in response_lower for phrase in no_info_phrases)
    
    def generate_answer(self, query: str, retrieved_schemes: List[Dict]) -> str:
        """
        Generate an answer based on the query and retrieved schemes
        
        Args:
            query: User's question
            retrieved_schemes: List of relevant schemes from vector search
            
        Returns:
            Generated answer string
        """
        if not retrieved_schemes:
            return "I don't have that information right now."
        
        try:
            # Create prompt
            prompt = self._create_prompt(query, retrieved_schemes)
            
            # Generate response using Gemini
            response = self.model.generate_content(prompt)
            
            # Safely extract text from response
            answer = ""
            if hasattr(response, 'text') and response.text:
                answer = str(response.text).strip()
            elif hasattr(response, 'candidates') and response.candidates:
                # Alternative response format
                try:
                    answer = str(response.candidates[0].content.parts[0].text).strip()
                except (AttributeError, IndexError, KeyError):
                    answer = ""
            else:
                # Fallback if response format is unexpected
                answer = str(response).strip() if response else ""
            
            # Ensure answer is not empty
            if not answer or len(answer.strip()) == 0:
                answer = "I don't have that information right now."
            
            # CRITICAL FIX: Remove ALL double colons (::) from ENTIRE answer immediately after LLM generation
            # Simple global replacement - removes ALL :: from everywhere
            while '::' in answer:
                answer = answer.replace('::', ':')
            
            # Post-process: if LLM says "no information" but we have schemes, try to be more lenient
            # Check if answer contains no-info phrases
            if self._check_no_info(answer, query) and retrieved_schemes:
                # Double-check: maybe the LLM was too strict
                # Check if any scheme name has keywords matching the query
                query_lower = query.lower()
                query_keywords = [w for w in query_lower.split() if len(w) > 3]
                
                for scheme in retrieved_schemes:
                    scheme_name = scheme.get('Scheme Name', '').lower()
                    scheme_name_clean = scheme_name.replace('(maharashtra)', '').replace('(urban)', '').replace('(rural)', '').strip()
                    scheme_keywords = [w for w in scheme_name_clean.split() if len(w) > 3]
                    
                    # If at least 2 significant words match, the scheme is likely relevant
                    matching = set(query_keywords).intersection(set(scheme_keywords))
                    if len(matching) >= 2:
                        # LLM might have been too strict, return a helpful message
                        scheme_name_full = scheme.get('Scheme Name', 'Unknown Scheme')
                        return f"I found information about **{scheme_name_full}** in the database. Please try rephrasing your question or asking about: eligibility, benefits, application process, or documents required for this scheme."
            
            return answer
        
        except Exception as e:
            print(f"Error generating answer: {e}")
            # Don't immediately say no information on error - return error context
            return f"An error occurred while generating the answer. Please try again or rephrase your question."
    
    def is_query_about_scheme_name(self, query: str) -> bool:
        """
        Check if the query seems to be about a specific scheme by name
        This helps determine the response format
        
        Args:
            query: User's question
            
        Returns:
            True if query appears to be about a scheme name
        """
        query_lower = query.lower()
        scheme_keywords = ["tell me about", "information about", "details about", "about the scheme"]
        return any(keyword in query_lower for keyword in scheme_keywords)


def get_qa_system(api_key: str) -> QASystem:
    """
    Factory function to create QA system
    
    Args:
        api_key: Google Gemini API key
        
    Returns:
        QASystem instance
    """
    return QASystem(api_key)

