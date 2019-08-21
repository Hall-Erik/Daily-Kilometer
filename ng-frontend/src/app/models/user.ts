import { Profile } from './profile';
import { Gear } from './gear';

export class User {
    pk: number;
    username: string;
    email: string;
    profile: Profile;
    gear: Gear[];

    public constructor(init?: Partial<User>) {
        Object.assign(this, init);
    }
}