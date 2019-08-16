import { Profile } from './profile';

export class User {
    pk: number;
    username: string;
    email: string;
    profile: Profile;

    public constructor(init?: Partial<User>) {
        Object.assign(this, init);
    }
}