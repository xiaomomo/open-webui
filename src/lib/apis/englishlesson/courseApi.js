import { WEBUI_API_BASE_URL } from '$lib/constants';

export async function fetchCourses() {
	try {
		const response = await fetch(`${WEBUI_API_BASE_URL}/fredisalesson/fredisalessons`);
		if (!response.ok) throw new Error('Failed to fetch courses');
		return await response.json();
	} catch (error) {
		console.error('Error fetching courses:', error);
		return [];
	}
}