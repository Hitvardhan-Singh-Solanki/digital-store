export interface Purchase {
  order_id: string;
  item: Item;
  timestamp: string;
}

export interface User {
  id: string;
  username: string;
}

export interface Item {
  id: number;
  name: string;
  description: string;
  price: number;
}
