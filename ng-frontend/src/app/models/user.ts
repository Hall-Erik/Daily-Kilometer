import { Profile } from './profile';
import { Gear } from './gear';

export class User {
    pk: number;
    username: string;
    email: string;
    profile: Profile;
    gear: Gear[];

    gravatar_url: string;

    public constructor(init?: Partial<User>) {
        Object.assign(this, init);
    }
}