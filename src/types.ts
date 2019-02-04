interface Message {
  id: number;
  username: string;
  message: string;
  timestamp: Date;
}

interface DictionaryEntry {
  word: string;
  meaning: string;
  country: string;
}

interface User {
  username: string;
  country: string;
}

export {
  Message,
  DictionaryEntry,
  User,
};
