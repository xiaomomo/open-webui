import type { PageLoad } from './$types';
import { error } from '@sveltejs/kit';

export const load: PageLoad = async ({ params }) => {
    if (!params.lessonUnitId) {
        throw error(404, 'Lesson unit not found');
    }

    return {
        lessonUnitId: params.lessonUnitId
    };
}; 