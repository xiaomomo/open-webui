import { WEBUI_API_BASE_URL } from '$lib/constants';


export interface Choice {
	id: string;
	text: string;
	nextScene?: string;
}

export interface Scene {
	id: string;
	text: string;
	type: 'input' | 'choice';
	choices?: Choice[];
	image?: string;
	nextScene?: string;
}

export async function getGameResponse() {
	try {
		const response = await fetch(`${WEBUI_API_BASE_URL}/fredisalesson/fredisalessons`);
		if (!response.ok) throw new Error('Failed to fetch courses');
		return await response.json();
	} catch (error) {
		console.error('Error fetching courses:', error);
		return [];
	}
}
