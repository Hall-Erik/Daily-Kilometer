import { User } from './user';

export class Gear {
    pk: number;
    name: string;
    start_distance: number;
    start_units: string;
    date_added: string;
    date_retired: string;
    user: User;

    public constructor(init?: Partial<Gear>) {
        Object.assign(this, init);
    }
}