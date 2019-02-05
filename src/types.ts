interface Room {
  uid: string;
  name: string;
  created: Date;
}

interface Message {
  id: number;
  username: string;
  message: string;
  timestamp: Date;
}

interface EntrySubmission {
  word: string;
  meaning: string;
}

interface DictionaryEntry extends EntrySubmission {
  id: number;
  country: string;
}

interface Session {
  username: string;
  country: string;
}

interface UserChanged extends Session {
  action: string;
}

export {
  Message,
  EntrySubmission,
  DictionaryEntry,
  Session,
  Room,
  UserChanged,
};
