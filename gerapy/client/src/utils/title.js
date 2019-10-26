import defaultSettings from '../../src/settings'

const title = defaultSettings.title || 'Gerapy'

export function getPageTitle(pageTitle) {
    if (pageTitle) {
        return `${pageTitle} - ${title}`
    }
    return `${title}`
}
