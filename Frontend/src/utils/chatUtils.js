import { LOAN_OPTIONS, CONVERSATION_START } from './chatbotData';
import { getNextMessageId } from './messageCounter';
// import TransactionTable from '@/components/chat/Table';


function generateTableHtml(data) {
  if (!data || !Array.isArray(data)) return '';

  // Extracting headers from the first object assuming all objects have the same structure
  const headers = Object.keys(data[0]);

  let htmlContent = `<table class="border-collapse border border-gray-200">
                      <thead>
                        <tr class="bg-gray-100">`;

  // Generating table headers
  headers.forEach(header => {
    htmlContent += `<th class="border border-gray-300 p-2">${header}</th>`;
  });

  htmlContent += `</tr>
                </thead>
                <tbody>`;

  // Generating table rows
  data.forEach(item => {
    htmlContent += `<tr class="bg-white">`;
    headers.forEach(header => {
      htmlContent += `<td class="border border-gray-300 p-2">${item[header]}</td>`;
    });
    htmlContent += `</tr>`;
  });

  htmlContent += `</tbody>
                  </table>`;

  return htmlContent;
}


export const createNewAssistantMessage = (content, options = null, reference = null) => {
  const newMessage = {
    id: getNextMessageId(),
    content: content || '',
    role: 'assistant',
  };

  if (options) {
    newMessage.options = options;
  }
  if (reference) {
    newMessage.reference = reference;
  }

  return newMessage;
};

export const createNewUserMessage = (content) => {
  const newMessage = {
    id: getNextMessageId(),
    content,
    role: 'user',
  };
  return newMessage;
};

export const responseConditions = [
  {
    check: (message, _) => CONVERSATION_START.includes(message),
    response: () => ({ content: 'Is a pleasure! What is your username?' }),
  },
  {
    check: (_, question) => question.includes('username'),
    response: () => ({ content: 'What is your password?' }),
  },
  {
    check: (_, question) => question.includes('password'),
    response: (context) => ({
      content: `Welcome ${context.user}! I'm your assistant, how can I help you?`,
    }),
  },
  {
    check: (message, _) => LOAN_OPTIONS.some(({ response }) => response === message),
    response: (context) => {
      const loanOption = LOAN_OPTIONS.find(({ response }) => response === context.message);
      return {
        content: loanOption.description,
        reference: loanOption.reference,
      };
    },
  },
  {
    check: (message, _) => message.includes('loan'),
    response: () => ({
      content: 'Loan options:',
      options: LOAN_OPTIONS,
    }),
  },
];


export const getAIBotResponse = async (message) => {
  try {
    const response = await fetch('http://localhost:5002/query', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ query: message }),
    });

    if (!response.ok) {
      throw new Error('Network response was not ok');
    }

    const data = await response.json();
    console.log('API response:', data);
    // if (data.highlight){
    //   return { content: data.highlight };
    // }
    // if (data.answer){
    //   return { content: data.answer };
    // }
    // if (data.message){
    //   return { content: data.message };
    // }
    if (data.message && data.message.includes('Missing required parameters')) {
      // Handle missing parameters case
      return { content: 'Please provide the required parameters.', required_params: data.required_params };
    } 
    else {
      // Handle regular response case
      if (data.highlight) {
        return { content: data.highlight };
      }
      if (data.answer) {
        return { content: data.answer };
      }
      // check if data.message is array

      if (data.message && Array.isArray(data.message)) {
        return { content: generateTableHtml(data.message) };
      }
      if (data.message) {
        return { content: data.message };
      }
    }

  } catch (error) {
    console.error('API error:', error);
    return { content: 'I am sorry, I cannot help you with that.' };
  }
};


export const firstMessage = {
  id: getNextMessageId(),
  content: 'Hello! 👋',
  role: 'assistant',
};
